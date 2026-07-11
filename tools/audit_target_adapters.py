"""Read-only auditor for target Project OS adoption state and adapter drift.

This diagnostic checks target-repository adapters. It does not validate the
kernel itself, edit target files, grant permission, or mutate git/GitHub state.

Exit codes: 0 = no findings, 1 = findings, 2 = tooling or evidence error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_METADATA = (
    "PROJECT_NAME",
    "REPOSITORY_NAME",
    "REPOSITORY_LOCAL_PATH",
    "DEFAULT_BRANCH",
    "WORK_BRANCH_PATTERN",
    "PM_FACING_LANGUAGE",
    "KERNEL_REPOSITORY",
    "KERNEL_LOCAL_PATH",
    "KERNEL_VERSION_ADOPTED",
)

CANONICAL_HEADINGS = {
    "AGENTS.md": {
        "Contract",
        "Contrato",
        "Repository identity",
        "Identidad del repositorio",
        "Kernel resolution",
        "Resolucion del kernel",
        "Resolución del kernel",
        "Outputs y artefactos",
        "Live state",
        "Estado vivo",
        "Evidencia viva",
        "Seguridad y validacion",
        "Seguridad y validación",
        "Project-specific notes",
        "Notas especificas del proyecto",
        "Notas específicas del proyecto",
        "Notas propias del target",
        "Notas propias del repositorio",
    },
    "BROWSER_CHAT.md": {
        "Contract",
        "Contrato",
        "Repository identity",
        "Identidad del repositorio",
        "Kernel resolution",
        "Resolucion del kernel",
        "Resolución del kernel",
        "Outputs y artefactos",
        "Live state",
        "Estado vivo",
        "Drafting interface",
        "Interfaz de drafting",
        "Seguridad y validacion",
        "Seguridad y validación",
        "Project-specific notes",
        "Notas especificas del proyecto",
        "Notas específicas del proyecto",
        "First-message activation",
        "Activacion del primer mensaje",
        "Activación del primer mensaje",
        "Resolución y evidencia",
        "Notas propias del target",
    },
    "CLAUDE.md": set(),
    "GEMINI.md": set(),
}

METADATA_PATTERN = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$")
PLACEHOLDER_PATTERN = re.compile(r"\{\{.*?\}\}|<[^>]+>")
SHA_PATTERN = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
GITHUB_ISSUE_URL_PATTERN = re.compile(
    r"https?://github\.com/([^/\s]+)/([^/\s]+)/issues/(\d+)\b", re.IGNORECASE
)
GITHUB_PR_URL_PATTERN = re.compile(
    r"https?://github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)\b", re.IGNORECASE
)
GITHUB_COMMIT_URL_PATTERN = re.compile(
    r"https?://github\.com/([^/\s]+)/([^/\s]+)/commit/[0-9a-f]{7,40}\b", re.IGNORECASE
)
ROADMAP_ANCHOR_PATTERN = re.compile(
    r"(?:https?://github\.com/([^/\s]+)/([^/\s]+)/issues/(\d+)\b)|(?:#(\d+)\b)", re.IGNORECASE
)
VERSION_PATTERN = re.compile(r"^(?:v?\d+(?:\.\d+)+(?:[-+][A-Za-z0-9._-]+)?|[0-9a-f]{40})$", re.IGNORECASE)
VAGUE_VERSION_VALUES = {"current", "latest", "last updated", "last-updated", "up to date", "updated"}

LIVE_STATE_PATTERNS = (
    ("TAA-LIVE-BRANCH", re.compile(r"\b(?:current|active)\s+branch\b|\bbranch\s+state\b|\bon\s+branch\b", re.I)),
    ("TAA-LIVE-PR", re.compile(r"\b(?:current|active|open|closed|merged)\s+(?:pr|pull request)\b", re.I)),
    (
        "TAA-LIVE-VALIDATION",
        re.compile(r"\bvalidation\s+(?:passed|failed|green|red|result|results)\b|\btests\s+(?:passed|failed)\b", re.I),
    ),
    ("TAA-LIVE-RELEASE", re.compile(r"\brelease[- ]readiness\b|\brelease\s+ready\b|\bready\s+to\s+release\b", re.I)),
)

PROHIBITION_MARKERS = (
    "must not store",
    "must not",
    "never trust",
    "never store",
    "no issue/pr/branch",
    "no shas",
    "no review status",
    "no release status",
    "do not store",
)

PROTECTED_NOTES_HEADING = "Project-specific notes"
PROTECTED_NOTES_HEADINGS = {
    PROTECTED_NOTES_HEADING,
    "Notas especificas del proyecto",
    "Notas específicas del proyecto",
    "Notas propias del target",
    "Notas propias del repositorio",
}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    file: str
    line: int | None
    message: str
    evidence: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
        }

    def render(self) -> str:
        location = self.file if self.line is None else f"{self.file}:{self.line}"
        suffix = f" Evidence: {self.evidence}" if self.evidence else ""
        return f"{self.code} [{self.severity}] {location}: {self.message}{suffix}"


@dataclass(frozen=True)
class Source:
    name: str
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


@dataclass(frozen=True)
class Section:
    heading: str
    line: int
    body: tuple[tuple[int, str], ...]


class AuditError(RuntimeError):
    """Tooling or unreadable evidence error."""


def _read_text(path: Path, name: str, required: bool = True) -> Source | None:
    if not path.exists():
        if required:
            raise AuditError(f"required adapter not found: {path}")
        return None
    try:
        return Source(name=name, text=path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise AuditError(f"could not read {path}: {exc}") from exc


def _git_show(target: Path, ref: str, rel_path: str, required: bool = True) -> Source | None:
    cmd = ["git", "-C", str(target), "show", f"{ref}:{rel_path}"]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        if required:
            detail = proc.stderr.strip() or proc.stdout.strip() or f"git show failed for {ref}:{rel_path}"
            raise AuditError(detail)
        return None
    return Source(name=rel_path, text=proc.stdout)


def _load_repo_sources(target: Path, ref: str | None = None) -> dict[str, Source]:
    if ref:
        agents = _git_show(target, ref, "AGENTS.md", required=False)
        claude = _git_show(target, ref, "CLAUDE.md", required=False)
        gemini = _git_show(target, ref, "GEMINI.md", required=False)
    else:
        agents = _read_text(target / "AGENTS.md", "AGENTS.md", required=False)
        claude = _read_text(target / "CLAUDE.md", "CLAUDE.md", required=False)
        gemini = _read_text(target / "GEMINI.md", "GEMINI.md", required=False)
    sources = {}
    if agents is not None:
        sources["AGENTS.md"] = agents
    if claude is not None:
        sources["CLAUDE.md"] = claude
    if gemini is not None:
        sources["GEMINI.md"] = gemini
    return sources


def _parse_metadata(source: Source) -> dict[str, list[tuple[int, str]]]:
    metadata: dict[str, list[tuple[int, str]]] = {}
    for line_no, line in enumerate(source.lines, start=1):
        match = METADATA_PATTERN.match(line.strip())
        if match:
            metadata.setdefault(match.group(1), []).append((line_no, match.group(2)))
    return metadata


def _line_for(metadata: dict[str, list[tuple[int, str]]], field: str) -> int | None:
    values = metadata.get(field, [])
    return values[0][0] if values else None


def _metadata_value(metadata: dict[str, list[tuple[int, str]]], field: str) -> str | None:
    values = metadata.get(field, [])
    return values[0][1] if values else None


def _is_placeholder(value: str) -> bool:
    return not value.strip() or bool(PLACEHOLDER_PATTERN.search(value))


def _raw_expanded_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value)))


def _resolved_expanded_path(value: str) -> Path:
    return _raw_expanded_path(value).resolve()


def _check_metadata(source: Source, target: Path, expected_repo: str) -> list[Finding]:
    findings: list[Finding] = []
    metadata = _parse_metadata(source)
    previous_line = 0
    for field in REQUIRED_METADATA:
        values = metadata.get(field, [])
        if not values:
            findings.append(
                Finding("TAA-META-MISSING", "error", source.name, None, f"missing metadata field {field!r}")
            )
            continue
        if len(values) > 1:
            findings.append(
                Finding(
                    "TAA-META-DUPLICATE",
                    "error",
                    source.name,
                    values[1][0],
                    f"metadata field {field!r} appears more than once",
                    values[1][1],
                )
            )
        line_no, value = values[0]
        if _is_placeholder(value):
            findings.append(
                Finding("TAA-META-PLACEHOLDER", "error", source.name, line_no, f"metadata field {field!r} is not filled", value)
            )
        if line_no < previous_line:
            findings.append(
                Finding(
                    "TAA-META-ORDER",
                    "warning",
                    source.name,
                    line_no,
                    f"metadata field {field!r} is out of the standard order",
                    value,
                )
            )
        previous_line = max(previous_line, line_no)

    repo_name = _metadata_value(metadata, "REPOSITORY_NAME")
    if repo_name and repo_name != expected_repo:
        findings.append(
            Finding(
                "TAA-META-REPOSITORY",
                "error",
                source.name,
                _line_for(metadata, "REPOSITORY_NAME"),
                f"REPOSITORY_NAME must be {expected_repo!r}",
                repo_name,
            )
        )

    local_path = _metadata_value(metadata, "REPOSITORY_LOCAL_PATH")
    if local_path and not _is_placeholder(local_path):
        raw_local_path = _raw_expanded_path(local_path)
        try:
            if not raw_local_path.is_absolute():
                findings.append(
                    Finding(
                        "TAA-META-LOCAL-PATH",
                        "warning",
                        source.name,
                        _line_for(metadata, "REPOSITORY_LOCAL_PATH"),
                        "REPOSITORY_LOCAL_PATH must be absolute",
                        local_path,
                    )
                )
            elif _resolved_expanded_path(local_path) != target.resolve():
                findings.append(
                    Finding(
                        "TAA-META-LOCAL-PATH",
                        "warning",
                        source.name,
                        _line_for(metadata, "REPOSITORY_LOCAL_PATH"),
                        "REPOSITORY_LOCAL_PATH does not match the audited target checkout",
                        local_path,
                    )
                )
        except RuntimeError:
            findings.append(
                Finding(
                    "TAA-META-LOCAL-PATH",
                    "warning",
                    source.name,
                    _line_for(metadata, "REPOSITORY_LOCAL_PATH"),
                    "REPOSITORY_LOCAL_PATH could not be resolved",
                    local_path,
                )
            )

    if (default_branch := _metadata_value(metadata, "DEFAULT_BRANCH")) and default_branch != "main":
        findings.append(
            Finding("TAA-META-DEFAULT-BRANCH", "warning", source.name, _line_for(metadata, "DEFAULT_BRANCH"), "DEFAULT_BRANCH should be main unless the target has an explicit exception", default_branch)
        )
    if (work_branch := _metadata_value(metadata, "WORK_BRANCH_PATTERN")) and work_branch != "work/*":
        findings.append(
            Finding("TAA-META-WORK-BRANCH", "warning", source.name, _line_for(metadata, "WORK_BRANCH_PATTERN"), "WORK_BRANCH_PATTERN should be work/* unless the target has an explicit exception", work_branch)
        )
    if (pm_language := _metadata_value(metadata, "PM_FACING_LANGUAGE")) and pm_language not in {"es", "en"}:
        findings.append(
            Finding("TAA-META-PM-LANGUAGE", "error", source.name, _line_for(metadata, "PM_FACING_LANGUAGE"), "PM_FACING_LANGUAGE must be es or en", pm_language)
        )
    if (kernel_repo := _metadata_value(metadata, "KERNEL_REPOSITORY")) and kernel_repo != "codefusion-repo/project-os-v2":
        findings.append(
            Finding("TAA-META-KERNEL-REPO", "error", source.name, _line_for(metadata, "KERNEL_REPOSITORY"), "KERNEL_REPOSITORY must point to codefusion-repo/project-os-v2", kernel_repo)
        )
    kernel_path = _metadata_value(metadata, "KERNEL_LOCAL_PATH")
    if kernel_path and not _is_placeholder(kernel_path):
        raw_kernel_path = _raw_expanded_path(kernel_path)
        try:
            if not raw_kernel_path.is_absolute():
                findings.append(
                    Finding("TAA-META-KERNEL-PATH", "warning", source.name, _line_for(metadata, "KERNEL_LOCAL_PATH"), "KERNEL_LOCAL_PATH must be absolute", kernel_path)
                )
        except RuntimeError:
            findings.append(
                Finding("TAA-META-KERNEL-PATH", "warning", source.name, _line_for(metadata, "KERNEL_LOCAL_PATH"), "KERNEL_LOCAL_PATH could not be resolved", kernel_path)
            )
    return findings


def _check_version_strategy(source: Source) -> list[Finding]:
    metadata = _parse_metadata(source)
    version = _metadata_value(metadata, "KERNEL_VERSION_ADOPTED")
    if not version or _is_placeholder(version):
        return []
    normalized = " ".join(version.strip().lower().split())
    line_no = _line_for(metadata, "KERNEL_VERSION_ADOPTED")
    if normalized == "tracks latest":
        return []
    if normalized in VAGUE_VERSION_VALUES or normalized.endswith(" latest"):
        return [
            Finding(
                "TAA-VERSION-VAGUE",
                "error",
                source.name,
                line_no,
                'KERNEL_VERSION_ADOPTED must be exactly "tracks latest" or a pinned version/immutable ref',
                version,
            )
        ]
    if VERSION_PATTERN.match(version.strip()):
        return []
    return [
        Finding(
            "TAA-VERSION-UNVERIFIED",
            "warning",
            source.name,
            line_no,
            "kernel version strategy is not recognized as rolling or pinned; resolvability is unverified",
            version,
        )
    ]


def _normalize_roadmap_anchor(expected_repo: str, line: str) -> str | None:
    matches = list(ROADMAP_ANCHOR_PATTERN.finditer(line))
    if not matches:
        return None
    match = matches[0]
    if match.group(4):
        return f"{expected_repo}#{match.group(4)}"
    owner, repo, number = match.group(1), match.group(2), match.group(3)
    return f"{owner}/{repo}#{number}"


def _all_roadmap_anchors(expected_repo: str, line: str) -> list[str]:
    anchors: list[str] = []
    for match in ROADMAP_ANCHOR_PATTERN.finditer(line):
        if match.group(4):
            anchors.append(f"{expected_repo}#{match.group(4)}")
        else:
            anchors.append(f"{match.group(1)}/{match.group(2)}#{match.group(3)}")
    return anchors


def _normalized_words(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(char for char in decomposed if not unicodedata.combining(char)).lower()


def _is_canonical_roadmap_label(line: str) -> bool:
    normalized = _normalized_words(line)
    return any(
        label in normalized
        for label in (
            "canonical roadmap issue",
            "roadmap canonico",
            "issue de roadmap canonico",
            "issue canonico de roadmap",
        )
    )


def _canonical_roadmap_lines(source: Source, expected_repo: str) -> list[tuple[int, str, list[str]]]:
    anchors: list[tuple[int, str, list[str]]] = []
    for line_no, line in enumerate(source.lines, start=1):
        if not _is_canonical_roadmap_label(line):
            continue
        normalized = _all_roadmap_anchors(expected_repo, line)
        if normalized:
            anchors.append((line_no, line.strip(), normalized))
    return anchors


def _check_roadmaps(full_sources: Iterable[Source], expected_repo: str) -> tuple[list[Finding], set[str]]:
    findings: list[Finding] = []
    canonical_anchors: set[str] = set()
    per_source: dict[str, str] = {}
    for source in full_sources:
        anchors = _canonical_roadmap_lines(source, expected_repo)
        anchor_count = sum(len(anchor_list) for _, _, anchor_list in anchors)
        if anchor_count == 0:
            findings.append(
                Finding(
                    "TAA-ROADMAP-MISSING",
                    "error",
                    source.name,
                    None,
                    "full adapter must contain exactly one canonical roadmap issue anchor",
                )
            )
            continue
        if anchor_count > 1:
            first_line = anchors[0][0] if anchors else None
            findings.append(
                Finding(
                    "TAA-ROADMAP-DUPLICATE",
                    "error",
                    source.name,
                    first_line,
                    "full adapter contains more than one canonical roadmap issue anchor",
                )
            )
        source_anchor = anchors[0][2][0]
        per_source[source.name] = source_anchor
        canonical_anchors.add(source_anchor)
        if not source_anchor.startswith(f"{expected_repo}#"):
            findings.append(
                Finding(
                    "TAA-ROADMAP-REPOSITORY",
                    "error",
                    source.name,
                    anchors[0][0],
                    f"roadmap anchor must point to {expected_repo}",
                    anchors[0][1],
                )
            )
    if len(set(per_source.values())) > 1:
        for source_name, anchor in sorted(per_source.items()):
            findings.append(
                Finding(
                    "TAA-ROADMAP-MISMATCH",
                    "error",
                    source_name,
                    None,
                    "supplied full adapters do not agree on the same roadmap anchor",
                    anchor,
                )
            )
    return findings, canonical_anchors


def _is_prohibition(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in PROHIBITION_MARKERS)


def _is_canonical_roadmap_line(line: str, expected_repo: str, canonical_anchors: set[str]) -> bool:
    if not _is_canonical_roadmap_label(line):
        return False
    anchor = _normalize_roadmap_anchor(expected_repo, line)
    return anchor in canonical_anchors if anchor else False


def _check_live_state(source: Source, expected_repo: str, canonical_anchors: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    metadata = _parse_metadata(source)
    version_line = _line_for(metadata, "KERNEL_VERSION_ADOPTED")
    prohibition_paragraph = False
    for line_no, line in enumerate(source.lines, start=1):
        stripped = line.strip()
        if not stripped:
            prohibition_paragraph = False
            continue
        if _is_prohibition(stripped):
            prohibition_paragraph = True
            continue
        if prohibition_paragraph:
            continue
        canonical_roadmap = _is_canonical_roadmap_line(stripped, expected_repo, canonical_anchors)
        if line_no != version_line and SHA_PATTERN.search(stripped):
            findings.append(
                Finding("TAA-LIVE-SHA", "error", source.name, line_no, "durable commit SHA-like value found", stripped)
            )
        for match in GITHUB_ISSUE_URL_PATTERN.finditer(stripped):
            anchor = f"{match.group(1)}/{match.group(2)}#{match.group(3)}"
            if canonical_roadmap and anchor in canonical_anchors:
                continue
            findings.append(
                Finding("TAA-LIVE-ISSUE-URL", "error", source.name, line_no, "mutable GitHub issue URL found outside the canonical roadmap anchor", stripped)
            )
        if GITHUB_PR_URL_PATTERN.search(stripped):
            findings.append(
                Finding("TAA-LIVE-PR-URL", "error", source.name, line_no, "mutable GitHub pull request URL found", stripped)
            )
        if GITHUB_COMMIT_URL_PATTERN.search(stripped):
            findings.append(
                Finding("TAA-LIVE-COMMIT-URL", "error", source.name, line_no, "mutable GitHub commit URL found", stripped)
            )
        for code, pattern in LIVE_STATE_PATTERNS:
            if pattern.search(stripped):
                findings.append(Finding(code, "warning", source.name, line_no, "likely durable live state found", stripped))
    return findings


def _check_compact_bootloader(source: Source, adapter_name: str, code_prefix: str) -> list[Finding]:
    text = source.text.lower()
    findings: list[Finding] = []
    if "agents.md" not in text:
        findings.append(
            Finding(
                f"TAA-{code_prefix}-DELEGATION",
                "warning",
                source.name,
                None,
                f"{adapter_name} should delegate repository-wide behavior to AGENTS.md",
            )
        )
    full_metadata_count = sum(1 for field in REQUIRED_METADATA if re.search(rf"^{field}\s*=", source.text, re.M))
    if full_metadata_count >= 4:
        findings.append(
            Finding(
                f"TAA-{code_prefix}-FULL-METADATA",
                "warning",
                source.name,
                None,
                f"{adapter_name} should stay compact and delegate instead of repeating the full metadata block",
            )
        )
    return findings


def _check_adoption_state(sources: dict[str, Source]) -> list[Finding]:
    findings: list[Finding] = []
    if "AGENTS.md" not in sources:
        findings.append(
            Finding(
                "TAA-ADOPTION-AGENTS-MISSING",
                "error",
                "AGENTS.md",
                None,
                "target adoption is missing AGENTS.md; draft only unless mode and exact PM approval permit adapter bootstrap",
            )
        )
    if "CLAUDE.md" not in sources:
        findings.append(
            Finding(
                "TAA-ADOPTION-CLAUDE-MISSING",
                "warning",
                "CLAUDE.md",
                None,
                "target adoption is missing CLAUDE.md; bootstrap scope is limited to adapters only when writes are approved",
            )
        )
    if "GEMINI.md" not in sources:
        findings.append(
            Finding(
                "TAA-ADOPTION-GEMINI-MISSING",
                "warning",
                "GEMINI.md",
                None,
                "target adoption is missing GEMINI.md; bootstrap scope is limited to adapters only when writes are approved",
            )
        )
    return findings


def _parse_sections(source: Source) -> dict[str, Section]:
    sections: dict[str, Section] = {}
    current: str | None = None
    current_line = 0
    body: list[tuple[int, str]] = []
    for line_no, line in enumerate(source.lines, start=1):
        match = re.match(r"^\s*##+\s+(.+?)\s*$", line)
        if match:
            if current is not None:
                sections[current] = Section(current, current_line, tuple(body))
            current = match.group(1).strip()
            current_line = line_no
            body = []
        elif current is not None:
            body.append((line_no, line.rstrip()))
    if current is not None:
        sections[current] = Section(current, current_line, tuple(body))
    return sections


def _significant_lines(section: Section | None) -> list[tuple[int, str]]:
    if section is None:
        return []
    lines: list[tuple[int, str]] = []
    for line_no, line in section.body:
        stripped = line.strip()
        if not stripped or PLACEHOLDER_PATTERN.search(stripped):
            continue
        lines.append((line_no, stripped))
    return lines


def _section_identity(heading: str) -> str:
    if heading in PROTECTED_NOTES_HEADINGS:
        return PROTECTED_NOTES_HEADING
    return heading


def _check_overlay_removals(base: Source, head: Source) -> list[Finding]:
    findings: list[Finding] = []
    base_sections = _parse_sections(base)
    head_sections = _parse_sections(head)
    head_sections_by_identity = {
        _section_identity(heading): section for heading, section in head_sections.items()
    }
    canonical = CANONICAL_HEADINGS.get(base.name, set())

    for heading, section in sorted(base_sections.items(), key=lambda item: item[1].line):
        protected = heading not in canonical or heading in PROTECTED_NOTES_HEADINGS
        if not protected:
            continue
        base_lines = _significant_lines(section)
        if not base_lines:
            continue
        head_section = head_sections_by_identity.get(_section_identity(heading))
        if head_section is None:
            findings.append(
                Finding(
                    "TAA-OVERLAY-SECTION-REMOVED",
                    "error",
                    f"{base.name}@base",
                    section.line,
                    f"protected target-owned section {heading!r} was removed",
                    heading,
                )
            )
            continue
        head_text = "\n".join(line for _, line in _significant_lines(head_section))
        for line_no, protected_line in base_lines:
            if protected_line not in head_text:
                findings.append(
                    Finding(
                        "TAA-OVERLAY-CONTENT-REMOVED",
                        "warning",
                        f"{base.name}@base",
                        line_no,
                        f"protected target-owned content under {heading!r} was removed or rewritten",
                        protected_line,
                    )
                )
    return findings


def _sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda f: (f.file, f.line if f.line is not None else -1, f.code, f.message, f.evidence))


def audit_target_adapters(
    target: Path | str,
    expected_repository: str,
    browser_chat: Source | None = None,
    base_ref: str | None = None,
    head_ref: str | None = None,
) -> list[Finding]:
    target_path = Path(target).resolve()
    if not target_path.is_dir():
        raise AuditError(f"target checkout is not a directory: {target_path}")

    findings: list[Finding] = []
    head_sources = _load_repo_sources(target_path, ref=head_ref)
    findings.extend(_check_adoption_state(head_sources))
    full_sources = [head_sources["AGENTS.md"]] if "AGENTS.md" in head_sources else []
    if browser_chat is not None:
        full_sources.append(browser_chat)

    for source in full_sources:
        findings.extend(_check_metadata(source, target_path, expected_repository))
        findings.extend(_check_version_strategy(source))
    if "CLAUDE.md" in head_sources:
        findings.extend(_check_compact_bootloader(head_sources["CLAUDE.md"], "CLAUDE.md", "CLAUDE"))
    if "GEMINI.md" in head_sources:
        findings.extend(_check_compact_bootloader(head_sources["GEMINI.md"], "GEMINI.md", "GEMINI"))

    terminal_sources = [head_sources["AGENTS.md"]] if "AGENTS.md" in head_sources else []
    roadmap_findings, canonical_anchors = _check_roadmaps(terminal_sources, expected_repository)
    findings.extend(roadmap_findings)
    for source in list(head_sources.values()) + ([browser_chat] if browser_chat else []):
        findings.extend(_check_live_state(source, expected_repository, canonical_anchors))

    if base_ref:
        base_sources = _load_repo_sources(target_path, ref=base_ref)
        for name, base_source in base_sources.items():
            head_source = head_sources.get(name)
            if head_source is not None:
                findings.extend(_check_overlay_removals(base_source, head_source))

    return _sorted_findings(findings)


def _load_browser_chat(value: str) -> Source:
    if value == "-":
        return Source(name="BROWSER_CHAT.md", text=sys.stdin.read())
    path = Path(value)
    try:
        return Source(name="BROWSER_CHAT.md", text=path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise AuditError(f"could not read browser-chat adapter {path}: {exc}") from exc


def _emit_json(target: Path, repository: str, findings: list[Finding]) -> None:
    payload = {
        "tool": "tools.audit_target_adapters",
        "schema_version": 1,
        "target": str(target.resolve()),
        "repository": repository,
        "findings": [finding.as_dict() for finding in findings],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def _emit_human(findings: list[Finding]) -> None:
    for finding in findings:
        print(finding.render())
    print(f"target adapter audit: {'FAIL' if findings else 'OK'} ({len(findings)} finding(s))")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="target repository checkout to inspect")
    parser.add_argument("--repository", required=True, help="expected target repository identity, e.g. owner/name")
    parser.add_argument("--browser-chat", help="full browser-chat adapter file, or '-' to read it from stdin")
    parser.add_argument("--base-ref", help="optional git ref to compare protected overlays against")
    parser.add_argument("--head-ref", help="optional git ref to audit instead of the worktree")
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    args = parser.parse_args(argv)

    target = Path(args.target)
    try:
        browser_chat = _load_browser_chat(args.browser_chat) if args.browser_chat else None
        findings = audit_target_adapters(
            target=target,
            expected_repository=args.repository,
            browser_chat=browser_chat,
            base_ref=args.base_ref,
            head_ref=args.head_ref,
        )
    except AuditError as exc:
        print(f"tooling error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        _emit_json(target, args.repository, findings)
    else:
        _emit_human(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
