"""Read-only GitHub traceability auditor.

This diagnostic inspects explicitly selected GitHub issues and pull requests.
It reports traceability findings only; it never comments, edits, labels, closes,
merges, or otherwise mutates GitHub state.

Exit codes: 0 = no findings, 1 = findings, 2 = tooling or evidence error.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from difflib import SequenceMatcher
from fnmatch import fnmatch
from typing import Iterable, Sequence


REQUIRED_CLOSURE_SECTIONS = (
    "completion_evidence",
    "validation_evidence",
    "accepted_exceptions",
    "boundaries_preserved",
    "friction_note",
    "references",
)

CLOSURE_SECTION_LABELS = {
    "completion_evidence": "Completion evidence",
    "validation_evidence": "Validation evidence",
    "accepted_exceptions": "Accepted exceptions",
    "boundaries_preserved": "Boundaries preserved",
    "friction_note": "Friction note",
    "references": "References",
}

CLOSURE_SECTION_ALIASES = {
    "completion_evidence": (
        "Completion evidence",
        "Evidencia de completitud",
        "Evidencia de finalización",
        "Evidencia de cierre",
    ),
    "validation_evidence": ("Validation evidence", "Evidencia de validación"),
    "accepted_exceptions": ("Accepted exceptions", "Excepciones aceptadas"),
    "boundaries_preserved": ("Boundaries preserved", "Límites preservados"),
    "friction_note": ("Friction note", "Nota de fricción"),
    "references": ("References", "Referencias"),
}

CLOSURE_PACKET_SIGNAL_SECTIONS = frozenset(REQUIRED_CLOSURE_SECTIONS[:-1])

EMPTY_EXCEPTION_VALUES = {
    "none",
    "ninguna",
    "ninguno",
    "n a",
    "na",
    "not applicable",
    "sin excepciones",
    "no exceptions",
}

COMMAND_PATTERN = re.compile(
    r"(`[^`]*(?:python3|pytest|git diff|tools\.validate_kernel|audit_traceability|npm|cargo|go test|make|ruff|mypy)[^`]*`)"
    r"|^\s*(?:[-*]\s*)?(?:python3|pytest|npm|cargo|go\s+test|git\s+diff|make|ruff|mypy)\b",
    re.IGNORECASE,
)
RESULT_PATTERN = re.compile(
    r"\b(?:PASS|PASSED|OK|clean|success|succeeded|green|no findings|no finding|"
    r"exit(?:ed)?\s*0|return(?:ed)?\s*0|result:?\s*(?:pass|ok|clean|success)|"
    r"\d+\s+passed|0\s+failed|tests?\s+passed)\b",
    re.IGNORECASE,
)
SKIPPED_WITH_REASON_PATTERN = re.compile(
    r"\b(?:not\s+run|not-run|skipped|skip|omitted|no\s+ejecutad[ao]|no\s+se\s+ejecut[óo])\b"
    r".{0,120}\b(?:because|due\s+to|reason|blocked|not\s+applicable|n/a|porque|por|ya\s+que)\b",
    re.IGNORECASE,
)
PM_ACCEPTANCE_PATTERN = re.compile(
    r"\b(?:accept(?:ed|ance)?|approv(?:e|ed|es)|decision|acept(?:o|a|ada|adas)|aprueb(?:o|a)|aprobado)\b",
    re.IGNORECASE,
)
EXCEPTION_CONTEXT_PATTERN = re.compile(
    r"\b(?:exception|exceptions|excepcion|excepciones|validation|validacion|skip|skipped|not\s+run|ci)\b",
    re.IGNORECASE,
)

CLOSING_DIRECTIVE_PATTERN = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?|"
    r"cerr(?:ar|ado|ada|ados|adas)|cierr(?:a|an|e|en)|"
    r"resolv(?:io|ió|ido|ida)|resuelv(?:e|en|a|an)|"
    r"correg(?:ir|ido|ida|idos|idas|e))\b",
    re.IGNORECASE,
)
ISSUE_REF_PATTERN = re.compile(
    r"(?:https://github\.com/[^/\s]+/[^/\s]+/issues/|(?<![A-Za-z0-9/])#)(\d+)\b",
    re.IGNORECASE,
)
MULTI_OUTCOME_PATTERN = re.compile(
    r"\b(?:multiple|two|2)\s+outcomes?\b|"
    r"\bunrelated\s+(?:work|commit|change|item)\b|"
    r"\balso\s+includes?\s+unrelated\b|"
    r"\bseparate\s+(?:outcome|deliverable|work\s+item)\b|"
    r"\banother\s+(?:issue|work\s+item)\b",
    re.IGNORECASE,
)

PATH_TOKEN_PATTERN = re.compile(
    r"`([^`\n]+)`|"
    r"(?<![\w./-])("
    r"(?:\.github/workflows/[A-Za-z0-9_.-]+)|"
    r"(?:[A-Za-z0-9_.-]+/[\w./*-]+)|"
    r"(?:README(?:\.md)?|AGENTS\.md|CLAUDE\.md|GEMINI\.md|pyproject\.toml|package(?:-lock)?\.json|"
    r"requirements(?:-[\w.-]+)?\.txt|poetry\.lock|Pipfile\.lock|Dockerfile|docker-compose\.ya?ml)"
    r")(?![\w./-])"
)

PROTECTED_PREFIXES = (
    "project-os-es/kernel/",
    "project-os-es/operaciones/",
    "project-os-es/templates/",
    "project-os-es/adapters/",
    "project-os-es/docs/",
    "project-os-es/habilidades/",
    "kernel/",
    "adapters/",
    ".github/workflows/",
    "migrations/",
    "migration/",
    "deploy/",
    "deployment/",
    "infra/",
)
PROTECTED_FILENAMES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "poetry.lock",
    "Pipfile.lock",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}


class AuditError(RuntimeError):
    """Tooling or unreadable evidence error."""


@dataclass(frozen=True)
class Comment:
    id: int
    author_login: str
    body: str
    created_at: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    body: str
    state: str
    closed_at: str | None = None
    comments: tuple[Comment, ...] = ()
    url: str | None = None


@dataclass(frozen=True)
class ChangedFile:
    filename: str
    status: str = "modified"


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    body: str
    state: str
    comments: tuple[Comment, ...] = ()
    changed_files: tuple[ChangedFile, ...] = ()
    url: str | None = None


@dataclass(frozen=True)
class Section:
    key: str
    label: str
    line: int
    body: tuple[tuple[int, str], ...]

    @property
    def text(self) -> str:
        return "\n".join(line for _, line in self.body)


@dataclass(frozen=True)
class ClosurePacket:
    comment: Comment
    sections: dict[str, Section]

    @property
    def section_count(self) -> int:
        return len(self.sections)


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    confidence: str
    repository: str
    item_kind: str
    item_number: int
    message: str
    evidence: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "confidence": self.confidence,
            "repository": self.repository,
            "item": {"kind": self.item_kind, "number": self.item_number},
            "message": self.message,
            "evidence": list(self.evidence),
        }

    def render(self) -> str:
        item = f"{self.repository} {self.item_kind}#{self.item_number}"
        suffix = f" Evidence: {'; '.join(self.evidence)}" if self.evidence else ""
        return f"{self.code} [{self.severity} confidence={self.confidence}] {item}: {self.message}{suffix}"


def _normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    asciiish = "".join(char for char in decomposed if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9]+", " ", asciiish.lower())
    return " ".join(normalized.split())


NORMALIZED_CLOSURE_ALIASES = {
    _normalize_text(alias): key for key, aliases in CLOSURE_SECTION_ALIASES.items() for alias in aliases
}


def _strip_heading_markup(line: str) -> str:
    stripped = line.strip()
    stripped = re.sub(r"^\s{0,3}#{1,6}\s*", "", stripped)
    stripped = re.sub(r"^\s*[-*]\s*", "", stripped)
    stripped = stripped.strip()
    stripped = re.sub(r"^(\*\*|__)", "", stripped)
    stripped = re.sub(r"(\*\*|__)$", "", stripped)
    return stripped.strip(" \t:-#*_")


def _closure_section_key(line: str) -> str | None:
    candidate = _strip_heading_markup(line)
    if not candidate or len(candidate) > 80:
        return None
    return NORMALIZED_CLOSURE_ALIASES.get(_normalize_text(candidate))


def parse_closure_packet(comment: Comment) -> ClosurePacket | None:
    sections: dict[str, Section] = {}
    current_key: str | None = None
    current_label = ""
    current_line = 0
    current_body: list[tuple[int, str]] = []

    for line_no, line in enumerate(comment.body.splitlines(), start=1):
        key = _closure_section_key(line)
        if key is not None:
            if current_key is not None:
                sections[current_key] = Section(current_key, current_label, current_line, tuple(current_body))
            current_key = key
            current_label = CLOSURE_SECTION_LABELS[key]
            current_line = line_no
            current_body = []
            continue
        if current_key is not None:
            current_body.append((line_no, line.rstrip()))

    if current_key is not None:
        sections[current_key] = Section(current_key, current_label, current_line, tuple(current_body))

    if not sections or not (set(sections) & CLOSURE_PACKET_SIGNAL_SECTIONS):
        return None
    return ClosurePacket(comment=comment, sections=sections)


def _best_closure_packet(comments: Sequence[Comment]) -> ClosurePacket | None:
    packets = [packet for comment in comments if (packet := parse_closure_packet(comment)) is not None]
    if not packets:
        return None
    return sorted(packets, key=lambda packet: (packet.section_count, packet.comment.created_at or "", packet.comment.id))[-1]


def _is_closed(issue: Issue) -> bool:
    return issue.state.lower() == "closed"


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _section_significant_lines(section: Section | None) -> list[str]:
    if section is None:
        return []
    lines: list[str] = []
    for _, line in section.body:
        stripped = line.strip()
        if not stripped or stripped in {"```", "~~~"}:
            continue
        stripped = stripped.strip("-* \t")
        if stripped:
            lines.append(stripped)
    return lines


def _accepted_exceptions_empty(section: Section | None) -> bool:
    lines = _section_significant_lines(section)
    if not lines:
        return True
    normalized_lines = [_normalize_text(line) for line in lines]
    return all(line in EMPTY_EXCEPTION_VALUES for line in normalized_lines if line)


def _has_validation_result_or_skip(section: Section | None) -> bool:
    if section is None:
        return True
    text = section.text
    return bool(RESULT_PATTERN.search(text) or SKIPPED_WITH_REASON_PATTERN.search(text))


def _has_validation_command(section: Section | None) -> bool:
    return bool(section and COMMAND_PATTERN.search(section.text))


def _pm_accepted_exception(comments: Sequence[Comment], packet: ClosurePacket, pm_login: str | None) -> bool:
    if not pm_login:
        return False
    expected_login = pm_login.lower()
    for comment in comments:
        if comment.author_login.lower() != expected_login:
            continue
        if comment.id == packet.comment.id and "accepted_exceptions" in packet.sections:
            return True
        if PM_ACCEPTANCE_PATTERN.search(comment.body) and EXCEPTION_CONTEXT_PATTERN.search(comment.body):
            return True
    return False


def _finding(
    code: str,
    severity: str,
    confidence: str,
    repository: str,
    item_kind: str,
    item_number: int,
    message: str,
    evidence: Iterable[str] = (),
) -> Finding:
    return Finding(
        code=code,
        severity=severity,
        confidence=confidence,
        repository=repository,
        item_kind=item_kind,
        item_number=item_number,
        message=message,
        evidence=tuple(str(item) for item in evidence if str(item)),
    )


def analyze_issue(repository: str, issue: Issue, pm_login: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    if _is_closed(issue):
        packet = _best_closure_packet(issue.comments)
        if packet is None:
            findings.append(
                _finding(
                    "TRACE-CLOSURE-PACKET-MISSING",
                    "error",
                    "high",
                    repository,
                    "issue",
                    issue.number,
                    "closed issue has no qualifying closure packet",
                    [f"comments={len(issue.comments)}", f"closed_at={issue.closed_at or 'unknown'}"],
                )
            )
        else:
            missing = [key for key in REQUIRED_CLOSURE_SECTIONS if key not in packet.sections]
            for key in missing:
                findings.append(
                    _finding(
                        "TRACE-CLOSURE-SECTION-MISSING",
                        "error",
                        "high",
                        repository,
                        "issue",
                        issue.number,
                        f"closure packet is missing {CLOSURE_SECTION_LABELS[key]!r}",
                        [f"comment_id={packet.comment.id}"],
                    )
                )
            validation = packet.sections.get("validation_evidence")
            if _has_validation_command(validation) and not _has_validation_result_or_skip(validation):
                findings.append(
                    _finding(
                        "TRACE-VALIDATION-RESULT-MISSING",
                        "error",
                        "high",
                        repository,
                        "issue",
                        issue.number,
                        "validation evidence names a command without a concrete result or explicit not-run reason",
                        [f"comment_id={packet.comment.id}", "section=Validation evidence"],
                    )
                )
            exceptions = packet.sections.get("accepted_exceptions")
            if not _accepted_exceptions_empty(exceptions):
                if not pm_login:
                    findings.append(
                        _finding(
                            "TRACE-PM-LOGIN-MISSING",
                            "error",
                            "high",
                            repository,
                            "issue",
                            issue.number,
                            "accepted exceptions require an explicit configured PM login for verification",
                            [f"comment_id={packet.comment.id}"],
                        )
                    )
                elif not _pm_accepted_exception(issue.comments, packet, pm_login):
                    findings.append(
                        _finding(
                            "TRACE-EXCEPTION-PM-DECISION-MISSING",
                            "error",
                            "high",
                            repository,
                            "issue",
                            issue.number,
                            "accepted exceptions lack an explicit PM decision by the configured login",
                            [f"pm_login={pm_login}", f"comment_id={packet.comment.id}"],
                        )
                    )
            closed_at = _parse_timestamp(issue.closed_at)
            packet_at = _parse_timestamp(packet.comment.created_at)
            if closed_at and packet_at and packet_at > closed_at:
                findings.append(
                    _finding(
                        "TRACE-CLOSURE-PACKET-LATE",
                        "warning",
                        "high",
                        repository,
                        "issue",
                        issue.number,
                        "closure packet was posted after the issue closed timestamp",
                        [
                            f"comment_id={packet.comment.id}",
                            f"comment_created_at={packet.comment.created_at}",
                            f"issue_closed_at={issue.closed_at}",
                        ],
                    )
                )

    findings.extend(_duplicate_comment_findings(repository, "issue", issue.number, issue.comments))
    return _sorted_findings(findings)


def _normalize_markdown(body: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return _normalize_text(text)


def _duplicate_comment_findings(
    repository: str,
    item_kind: str,
    item_number: int,
    comments: Sequence[Comment],
) -> list[Finding]:
    findings: list[Finding] = []
    normalized = [(comment, _normalize_markdown(comment.body)) for comment in comments]
    normalized = [(comment, body) for comment, body in normalized if body]

    groups: dict[str, list[Comment]] = {}
    for comment, body in normalized:
        groups.setdefault(body, []).append(comment)
    exact_pairs: set[tuple[int, int]] = set()
    for body, grouped in sorted(groups.items(), key=lambda item: item[0]):
        if len(grouped) < 2:
            continue
        ids = tuple(sorted(comment.id for comment in grouped))
        for left in ids:
            for right in ids:
                if left < right:
                    exact_pairs.add((left, right))
        findings.append(
            _finding(
                "TRACE-DUPLICATE-COMMENT",
                "warning",
                "high",
                repository,
                item_kind,
                item_number,
                "exact duplicate comments found after Markdown normalization",
                [f"comment_ids={','.join(str(comment_id) for comment_id in ids)}", f"normalized={body[:80]}"],
            )
        )

    for index, (left_comment, left_body) in enumerate(normalized):
        if len(left_body) < 24:
            continue
        for right_comment, right_body in normalized[index + 1 :]:
            pair = tuple(sorted((left_comment.id, right_comment.id)))
            if pair in exact_pairs or len(right_body) < 24:
                continue
            ratio = SequenceMatcher(None, left_body, right_body).ratio()
            if ratio >= 0.9:
                findings.append(
                    _finding(
                        "TRACE-NEAR-DUPLICATE-COMMENT",
                        "warning",
                        "medium",
                        repository,
                        item_kind,
                        item_number,
                        "near-duplicate comments found after Markdown normalization",
                        [f"comment_ids={pair[0]},{pair[1]}", f"similarity={ratio:.3f}"],
                    )
                )
    return findings


def _issue_refs(text: str) -> set[int]:
    return {int(match.group(1)) for match in ISSUE_REF_PATTERN.finditer(text)}


def linked_issue_numbers(pr: PullRequest) -> set[int]:
    # Prefer the conventional issue reference in the title. Body prose often
    # names roadmap/follow-up issues and the PR itself, which are context rather
    # than the scope-bearing linked issue.
    title_refs = _issue_refs(pr.title) - {pr.number}
    if title_refs:
        return title_refs
    closing_refs: set[int] = set()
    for line in pr.body.splitlines():
        if CLOSING_DIRECTIVE_PATTERN.search(line):
            closing_refs.update(_issue_refs(line))
    if closing_refs:
        return closing_refs - {pr.number}
    body_refs = _issue_refs(pr.body) - {pr.number}
    return body_refs if len(body_refs) <= 1 else set()


def _multi_outcome_finding(repository: str, pr: PullRequest) -> Finding | None:
    text = f"{pr.title}\n{pr.body}\n" + "\n".join(comment.body for comment in pr.comments)
    evidence: list[str] = []
    confidence = "medium"

    closing_refs: set[int] = set()
    for line in text.splitlines():
        if CLOSING_DIRECTIVE_PATTERN.search(line):
            closing_refs.update(_issue_refs(line))
    if len(closing_refs) > 1:
        confidence = "high"
        evidence.append("multiple_closing_refs=" + ",".join(f"#{number}" for number in sorted(closing_refs)))

    phrase_match = MULTI_OUTCOME_PATTERN.search(text)
    if phrase_match:
        confidence = "high" if "unrelated" in phrase_match.group(0).lower() else confidence
        evidence.append(f"phrase={phrase_match.group(0).strip()}")

    numbered_refs: set[int] = set()
    for line in text.splitlines():
        if re.match(r"^\s*\d+[.)]\s+", line):
            numbered_refs.update(_issue_refs(line))
    if len(numbered_refs) > 1:
        evidence.append("numbered_deliverable_refs=" + ",".join(f"#{number}" for number in sorted(numbered_refs)))

    if not evidence:
        return None
    return _finding(
        "TRACE-PR-MULTI-OUTCOME",
        "warning",
        confidence,
        repository,
        "pr",
        pr.number,
        "pull request likely contains more than one outcome",
        evidence,
    )


def _parse_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if match:
            current = _normalize_text(match.group(1))
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {heading: "\n".join(lines) for heading, lines in sections.items()}


def _issue_section(issue: Issue, heading: str) -> str:
    return _parse_markdown_sections(issue.body).get(_normalize_text(heading), "")


def _clean_path_token(token: str) -> str | None:
    value = token.strip().strip(".,;:()[]{}<>\"'")
    value = value.removeprefix("./")
    if not value or "://" in value or value.startswith("#") or " " in value:
        return None
    if value == "README":
        return "README.md"
    if value.endswith("/**"):
        value = value[:-2]
    if value.endswith("*") and not value.endswith("/*"):
        return None
    if "/" not in value and value not in PROTECTED_FILENAMES and not re.search(r"\.[A-Za-z0-9]+$", value):
        return None
    return value


def _extract_paths(text: str) -> tuple[str, ...]:
    paths: set[str] = set()
    for match in PATH_TOKEN_PATTERN.finditer(text):
        token = match.group(1) or match.group(2) or ""
        cleaned = _clean_path_token(token)
        if cleaned:
            paths.add(cleaned)
    return tuple(sorted(paths))


def _path_matches(filename: str, pattern: str) -> bool:
    normalized = filename.removeprefix("./")
    candidate = pattern.removeprefix("./")
    if candidate == "README":
        candidate = "README.md"
    if candidate.endswith("/*"):
        return normalized.startswith(candidate[:-1])
    if candidate.endswith("/"):
        return normalized.startswith(candidate)
    if "*" in candidate:
        return fnmatch(normalized, candidate)
    return normalized == candidate or normalized.startswith(candidate.rstrip("/") + "/")


def _is_protected_file(filename: str) -> bool:
    return filename in PROTECTED_FILENAMES or any(filename.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def _file_scope_findings(repository: str, pr: PullRequest, issue: Issue | None) -> list[Finding]:
    if issue is None:
        return [
            _finding(
                "TRACE-PR-LINKED-ISSUE-MISSING",
                "error",
                "high",
                repository,
                "pr",
                pr.number,
                "pull request file-scope audit requires a linked issue scope",
                ["no linked issue body was available to the analyzer"],
            )
        ]

    scope_paths = _extract_paths(_issue_section(issue, "Scope"))
    out_of_scope_paths = _extract_paths(_issue_section(issue, "Out of scope"))
    findings: list[Finding] = []

    for changed in pr.changed_files:
        filename = changed.filename
        matched_out = [path for path in out_of_scope_paths if _path_matches(filename, path)]
        if matched_out:
            findings.append(
                _finding(
                    "TRACE-PR-OUT-OF-SCOPE-FILE",
                    "error",
                    "high",
                    repository,
                    "pr",
                    pr.number,
                    "changed file matches an explicit out-of-scope path",
                    [f"file={filename}", "out_of_scope=" + ",".join(matched_out)],
                )
            )
            continue

        matched_scope = [path for path in scope_paths if _path_matches(filename, path)]
        if matched_scope:
            continue

        if scope_paths:
            confidence = "high" if _is_protected_file(filename) else "medium"
            findings.append(
                _finding(
                    "TRACE-PR-OUT-OF-SCOPE-FILE",
                    "warning",
                    confidence,
                    repository,
                    "pr",
                    pr.number,
                    "changed file is not named by the linked issue scope",
                    [f"file={filename}", "scope_paths=" + ",".join(scope_paths)],
                )
            )
        elif _is_protected_file(filename):
            findings.append(
                _finding(
                    "TRACE-PR-OUT-OF-SCOPE-FILE",
                    "warning",
                    "low",
                    repository,
                    "pr",
                    pr.number,
                    "changed protected/high-impact file but the linked issue has no machine-checkable path boundary",
                    [f"file={filename}"],
                )
            )
    return findings


def analyze_pull_request(
    repository: str,
    pr: PullRequest,
    linked_issues: Sequence[Issue] = (),
) -> list[Finding]:
    findings: list[Finding] = []
    if multi := _multi_outcome_finding(repository, pr):
        findings.append(multi)

    issue_for_scope = linked_issues[0] if len(linked_issues) == 1 else None
    if pr.changed_files:
        findings.extend(_file_scope_findings(repository, pr, issue_for_scope))

    findings.extend(_duplicate_comment_findings(repository, "pr", pr.number, pr.comments))
    return _sorted_findings(findings)


def _sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda finding: (
            finding.repository,
            finding.item_kind,
            finding.item_number,
            finding.code,
            finding.message,
            finding.evidence,
        ),
    )


class GithubClient:
    """Read-only GitHub evidence loader backed by `gh api` GET requests."""

    def __init__(self, repository: str) -> None:
        if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repository):
            raise AuditError(f"repository must be owner/name: {repository!r}")
        self.repository = repository

    def ensure_ready(self) -> None:
        if shutil.which("gh") is None:
            raise AuditError("gh CLI not found")
        proc = subprocess.run(["gh", "auth", "status"], check=False, capture_output=True, text=True)
        if proc.returncode != 0:
            detail = proc.stderr.strip() or proc.stdout.strip() or "gh authentication failed"
            raise AuditError(detail)

    def _api_json(self, endpoint: str, fields: dict[str, str] | None = None) -> object:
        cmd = ["gh", "api", "--method", "GET"]
        cmd.append(endpoint)
        for key, value in sorted((fields or {}).items()):
            cmd.extend(["-f", f"{key}={value}"])
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if proc.returncode != 0:
            detail = proc.stderr.strip() or proc.stdout.strip() or f"gh api failed: {endpoint}"
            raise AuditError(detail)
        try:
            return json.loads(proc.stdout or "null")
        except json.JSONDecodeError as exc:
            raise AuditError(f"gh api returned invalid JSON for {endpoint}") from exc

    def _paged_list(self, endpoint: str) -> list[dict[str, object]]:
        items: list[dict[str, object]] = []
        page = 1
        per_page = 100
        while True:
            payload = self._api_json(endpoint, fields={"page": str(page), "per_page": str(per_page)})
            if not isinstance(payload, list):
                raise AuditError(f"unsupported paginated payload for {endpoint}")
            for item in payload:
                if not isinstance(item, dict):
                    raise AuditError(f"unsupported paginated item for {endpoint}")
                items.append(item)
            if len(payload) < per_page:
                break
            page += 1
        return items

    def fetch_issue(self, number: int) -> Issue:
        payload = self._api_json(f"/repos/{self.repository}/issues/{number}")
        if not isinstance(payload, dict):
            raise AuditError(f"unsupported issue payload for #{number}")
        if "pull_request" in payload:
            raise AuditError(f"#{number} is a pull request; use --pr for PR analysis")
        comments = self._fetch_issue_comments(number)
        return _issue_from_payload(payload, comments)

    def fetch_pull_request(self, number: int) -> PullRequest:
        payload = self._api_json(f"/repos/{self.repository}/pulls/{number}")
        if not isinstance(payload, dict):
            raise AuditError(f"unsupported pull request payload for #{number}")
        comments = self._fetch_issue_comments(number)
        files = self._fetch_pr_files(number, payload)
        return _pr_from_payload(payload, comments, files)

    def _fetch_issue_comments(self, number: int) -> tuple[Comment, ...]:
        payload = self._paged_list(f"/repos/{self.repository}/issues/{number}/comments")
        return tuple(_comment_from_payload(item) for item in payload)

    def _fetch_pr_files(self, number: int, pr_payload: dict[str, object]) -> tuple[ChangedFile, ...]:
        payload = self._paged_list(f"/repos/{self.repository}/pulls/{number}/files")
        expected = pr_payload.get("changed_files")
        if isinstance(expected, int) and expected != len(payload):
            raise AuditError(f"truncated PR file evidence for #{number}: expected {expected}, got {len(payload)}")
        return tuple(_file_from_payload(item) for item in payload)

    def search_range(self, since: str, until: str, kind: str, limit: int) -> tuple[list[int], list[int]]:
        qualifiers = {
            "issues": "type:issue",
            "prs": "type:pr",
            "both": "",
        }[kind]
        q = f"repo:{self.repository} {qualifiers} updated:{since}..{until}".strip()
        payload = self._api_json("/search/issues", fields={"q": q, "per_page": str(min(limit, 100))})
        if not isinstance(payload, dict):
            raise AuditError("unsupported search payload")
        if payload.get("incomplete_results"):
            raise AuditError("GitHub search returned incomplete results")
        total = payload.get("total_count")
        items = payload.get("items")
        if not isinstance(total, int) or not isinstance(items, list):
            raise AuditError("unsupported search fields")
        if total > limit or total > len(items):
            raise AuditError(f"bounded search returned {total} items; narrow the range or raise --limit")
        issue_numbers: list[int] = []
        pr_numbers: list[int] = []
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("number"), int):
                raise AuditError("unsupported search item fields")
            if "pull_request" in item:
                pr_numbers.append(int(item["number"]))
            else:
                issue_numbers.append(int(item["number"]))
        return sorted(issue_numbers), sorted(pr_numbers)


def _require(payload: dict[str, object], key: str, expected_type: type | tuple[type, ...]) -> object:
    value = payload.get(key)
    if value is None and type(None) in (expected_type if isinstance(expected_type, tuple) else ()):
        return value
    if not isinstance(value, expected_type):
        raise AuditError(f"unsupported or missing field {key!r}")
    return value


def _comment_from_payload(payload: dict[str, object]) -> Comment:
    user = payload.get("user")
    if not isinstance(user, dict) or not isinstance(user.get("login"), str):
        raise AuditError("unsupported or missing comment author field")
    return Comment(
        id=int(_require(payload, "id", int)),
        author_login=str(user["login"]),
        body=str(_require(payload, "body", str)),
        created_at=payload.get("created_at") if isinstance(payload.get("created_at"), str) else None,
        url=payload.get("html_url") if isinstance(payload.get("html_url"), str) else None,
    )


def _issue_from_payload(payload: dict[str, object], comments: tuple[Comment, ...]) -> Issue:
    return Issue(
        number=int(_require(payload, "number", int)),
        title=str(_require(payload, "title", str)),
        body=payload.get("body") if isinstance(payload.get("body"), str) else "",
        state=str(_require(payload, "state", str)),
        closed_at=payload.get("closed_at") if isinstance(payload.get("closed_at"), str) else None,
        comments=comments,
        url=payload.get("html_url") if isinstance(payload.get("html_url"), str) else None,
    )


def _file_from_payload(payload: dict[str, object]) -> ChangedFile:
    return ChangedFile(filename=str(_require(payload, "filename", str)), status=str(payload.get("status") or "modified"))


def _pr_from_payload(
    payload: dict[str, object],
    comments: tuple[Comment, ...],
    files: tuple[ChangedFile, ...],
) -> PullRequest:
    return PullRequest(
        number=int(_require(payload, "number", int)),
        title=str(_require(payload, "title", str)),
        body=payload.get("body") if isinstance(payload.get("body"), str) else "",
        state=str(_require(payload, "state", str)),
        comments=comments,
        changed_files=files,
        url=payload.get("html_url") if isinstance(payload.get("html_url"), str) else None,
    )


def _emit_json(repository: str, findings: list[Finding], audited: dict[str, list[int]]) -> None:
    payload = {
        "tool": "tools.audit_traceability",
        "schema_version": 1,
        "repository": repository,
        "audited": audited,
        "findings": [finding.as_dict() for finding in findings],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def _emit_human(findings: list[Finding]) -> None:
    for finding in findings:
        print(finding.render())
    print(f"traceability audit: {'FAIL' if findings else 'OK'} ({len(findings)} finding(s))")


def _valid_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid ISO date: {value}") from exc
    return value


def _collect_targets(args: argparse.Namespace, client: GithubClient) -> tuple[list[int], list[int]]:
    issue_numbers = sorted(set(args.issue or []))
    pr_numbers = sorted(set(args.pr or []))
    if args.since or args.until:
        if not args.since or not args.until:
            raise AuditError("--since and --until must be provided together")
        if args.since > args.until:
            raise AuditError("--since must be before or equal to --until")
        if args.limit < 1 or args.limit > 100:
            raise AuditError("--limit must be between 1 and 100")
        range_issues, range_prs = client.search_range(args.since, args.until, args.range_kind, args.limit)
        issue_numbers = sorted(set(issue_numbers) | set(range_issues))
        pr_numbers = sorted(set(pr_numbers) | set(range_prs))
    if not issue_numbers and not pr_numbers:
        raise AuditError("provide --issue, --pr, or a bounded --since/--until range")
    return issue_numbers, pr_numbers


def audit_repository(
    repository: str,
    issue_numbers: Sequence[int],
    pr_numbers: Sequence[int],
    pm_login: str | None,
    client: GithubClient,
) -> tuple[list[Finding], dict[str, list[int]]]:
    issues: dict[int, Issue] = {}
    findings: list[Finding] = []

    for number in issue_numbers:
        issue = client.fetch_issue(number)
        issues[number] = issue
        findings.extend(analyze_issue(repository, issue, pm_login=pm_login))

    for number in pr_numbers:
        pr = client.fetch_pull_request(number)
        linked: dict[int, Issue] = {}
        for linked_number in linked_issue_numbers(pr):
            if linked_number in issues:
                linked[linked_number] = issues[linked_number]
                continue
            linked[linked_number] = client.fetch_issue(linked_number)
        findings.extend(analyze_pull_request(repository, pr, linked_issues=tuple(linked.values())))

    audited = {"issues": sorted(issues), "prs": sorted(pr_numbers)}
    return _sorted_findings(findings), audited


def main(argv: list[str] | None = None, client_cls: type[GithubClient] = GithubClient) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="GitHub repository in owner/name form")
    parser.add_argument("--issue", type=int, action="append", help="issue number to audit; may be repeated")
    parser.add_argument("--pr", type=int, action="append", help="pull request number to audit; may be repeated")
    parser.add_argument("--since", type=_valid_date, help="bounded updated-at range start date, YYYY-MM-DD")
    parser.add_argument("--until", type=_valid_date, help="bounded updated-at range end date, YYYY-MM-DD")
    parser.add_argument("--range-kind", choices=("issues", "prs", "both"), default="both")
    parser.add_argument("--limit", type=int, default=25, help="maximum bounded range items, 1-100")
    parser.add_argument("--pm-login", help="authoritative PM login used to verify accepted exceptions")
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    args = parser.parse_args(argv)

    try:
        client = client_cls(args.repository)
        client.ensure_ready()
        issue_numbers, pr_numbers = _collect_targets(args, client)
        findings, audited = audit_repository(
            repository=args.repository,
            issue_numbers=issue_numbers,
            pr_numbers=pr_numbers,
            pm_login=args.pm_login,
            client=client,
        )
    except AuditError as exc:
        print(f"tooling error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        _emit_json(args.repository, findings, audited)
    else:
        _emit_human(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
