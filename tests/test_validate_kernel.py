"""Tests for the project-os-v2-min kernel validator and repo-shape guards."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from fnmatch import fnmatch
from pathlib import Path

import pytest

from tools.validate_kernel import validate_kernel

REPO_ROOT = Path(__file__).resolve().parent.parent


def codes(findings) -> set[str]:
    return {finding.code for finding in findings}


@pytest.fixture()
def kernel_copy(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "kernel", tmp_path / "kernel")
    return tmp_path


def mutate(root: Path, name: str, fn) -> None:
    path = root / "kernel" / name
    data = json.loads(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_real_kernel_passes() -> None:
    assert validate_kernel(REPO_ROOT) == []


def test_missing_kernel_dir_fails(tmp_path: Path) -> None:
    assert codes(validate_kernel(tmp_path)) == {"KMIN-001"}


def test_invalid_json_fails(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "actors.json").write_text("{not json", encoding="utf-8")
    assert "KMIN-001" in codes(validate_kernel(kernel_copy))


def test_load_order_missing_file(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "evidence.json").unlink()
    assert "KMIN-002" in codes(validate_kernel(kernel_copy))


def test_undeclared_kernel_file(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "extra.json").write_text('{"id": "kernel.extra", "family": "extra"}', encoding="utf-8")
    assert "KMIN-002" in codes(validate_kernel(kernel_copy))


def test_missing_entry_key(kernel_copy: Path) -> None:
    mutate(kernel_copy, "boundaries.json", lambda d: d["entries"][0].pop("rule"))
    assert "KMIN-003" in codes(validate_kernel(kernel_copy))


def test_duplicate_id(kernel_copy: Path) -> None:
    mutate(kernel_copy, "evidence.json", lambda d: d["entries"].append(dict(d["entries"][0])))
    assert "KMIN-004" in codes(validate_kernel(kernel_copy))


def test_unresolved_reference(kernel_copy: Path) -> None:
    mutate(kernel_copy, "workflows.json", lambda d: d["entries"][0]["required_evidence_refs"].append("evidence.does_not_exist"))
    assert "KMIN-005" in codes(validate_kernel(kernel_copy))


def test_non_canonical_status_reference(kernel_copy: Path) -> None:
    mutate(kernel_copy, "boundaries.json", lambda d: d["entries"][0].update(on_violation="status.maybe"))
    assert "KMIN-006" in codes(validate_kernel(kernel_copy))


def test_fifth_status_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "statuses.json",
        lambda d: d["entries"].append({"id": "status.deferred", "meaning": "extra status"}),
    )
    assert "KMIN-007" in codes(validate_kernel(kernel_copy))


def test_permission_grant_key_rejected(kernel_copy: Path) -> None:
    mutate(kernel_copy, "actors.json", lambda d: d["entries"][1].update(can_push=True))
    assert "KMIN-008" in codes(validate_kernel(kernel_copy))


def test_live_state_sha_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "manifest.json",
        lambda d: d.update(description="baseline " + "a1" * 20),
    )
    assert "KMIN-009" in codes(validate_kernel(kernel_copy))


def test_github_url_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "evidence.json",
        lambda d: d["entries"][0].update(satisfied_by="see github.com/example/repo/issues/1"),
    )
    assert "KMIN-009" in codes(validate_kernel(kernel_copy))


def test_browser_actor_write_mode_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "actors.json",
        lambda d: d["entries"][2]["allowed_mode_refs"].append("mode.delegated_commit_pr"),
    )
    assert "KMIN-010" in codes(validate_kernel(kernel_copy))


def test_size_budget_enforced(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "manifest.json",
        lambda d: d["size_budget"].update(kernel_total_bytes_max=100),
    )
    assert "KMIN-011" in codes(validate_kernel(kernel_copy))


# --- Repo-shape guards (prevent regressing the #287 simplification) ---------
#
# Deterministic checks that keep project-os-v2 a compact, portable kernel:
# console planning docs stay out, the actor model stays surface-only, command
# bundles never emit unsupported gh --json fields, and the command-bundle source
# keeps its normalized location. They guard repo shape only; no writes, no
# authority.

FORBIDDEN_CONSOLE_DOCS = (
    "docs/OPERATIONS_CATALOG.md",
    "docs/OPERATIONS_CONSOLE_IMPLEMENTATION_PLAN.md",
)
CANONICAL_ACTOR_IDS = {
    "actor.human_pm",
    "actor.terminal_agent",
    "actor.browser_chat",
    "actor.unknown",
}
FORBIDDEN_GH_JSON_FIELDS = {"stateReason", "merged"}
GH_JSON_PATTERN = re.compile(r"--json\s+([A-Za-z0-9_,]+)")
KERNEL_ID_PATTERN = re.compile(
    r"\b(?:status|actor|mode|boundary|evidence|workflow|output)\."
    r"(?!json\b|get\b|append\b)[A-Za-z0-9_*]+"
)
ROLE_ACTOR_ID_PATTERN = re.compile(r"\bactor\.(?:reviewer|qa|security|security_reviewer|asset|asset_creator)\b")
MARKDOWN_PATH_PATTERN = re.compile(r"`([^`\n]+)`")
SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "node_modules", ".venv"}

# Narrow allowlists for intentional negative fixtures, target-owned optional
# paths in copy-in adapters, and historical recovery references.
KERNEL_ID_REFERENCE_ALLOWLIST = {
    ("tests/test_validate_kernel.py", "evidence.does_not_exist"): "negative unresolved-reference fixture",
    ("tests/test_validate_kernel.py", "status.deferred"): "negative fifth-status fixture",
    ("tests/test_validate_kernel.py", "status.maybe"): "negative non-canonical-status fixture",
}
MARKDOWN_PATH_REFERENCE_ALLOWLIST = {
    ("adapters/AGENTS.target.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("adapters/BROWSER_CHAT.target.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("docs/DESIGN.md", "fuentes/"): "historical path recoverable from git history",
}


def _markdown_files() -> list[Path]:
    return [p for p in REPO_ROOT.rglob("*.md") if not (set(p.parts) & SKIP_DIRS)]


def _tracked_paths() -> set[str]:
    proc = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    return set(proc.stdout.splitlines())


def _tracked_text_files() -> list[Path]:
    suffixes = {".json", ".md", ".py", ".yml", ".yaml"}
    return [REPO_ROOT / rel for rel in sorted(_tracked_paths()) if Path(rel).suffix in suffixes]


def _kernel_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted((REPO_ROOT / "kernel").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data.get("id"), str):
            ids.add(data["id"])
        for entry in data.get("entries", []):
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                ids.add(entry["id"])
    return ids


def _kernel_entry(file_name: str, entry_id: str) -> dict:
    data = json.loads((REPO_ROOT / "kernel" / file_name).read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry["id"] == entry_id:
            return entry
    raise AssertionError(f"{entry_id} not found in {file_name}")


def _normalize_markdown_path_ref(token: str) -> str | None:
    value = token.strip().strip(",;:()[]{}\"'")
    if value.endswith(".") and not value.startswith("."):
        value = value[:-1]
    if (
        not value
        or " " in value
        or "{{" in value
        or "}}" in value
        or "<" in value
        or ">" in value
        or "$HOME" in value
        or "..." in value
        or value.startswith(("#", "/", "http://", "https://"))
    ):
        return None
    if value == "README":
        return "README.md"
    if value == "manifest.json":
        return "kernel/manifest.json"
    if value in {"artifacts.md", "route-prompt.md", "pm-command-bundle.md"}:
        return f"templates/{value}"
    if "/" not in value and (value.startswith(".") or Path(value).stem.isupper()):
        return None
    if re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", value) and "." not in value.rsplit("/", 1)[-1]:
        return None
    if value.startswith("tools.") and "/" not in value:
        return f"{value.replace('.', '/')}.py"
    if "/" not in value and not value.endswith((".md", ".json", ".py", ".yml", ".yaml")):
        return None
    if value.startswith(("work/", "org/", "owner/", "repo/")):
        return None
    return value


def _tracked_ref_exists(ref: str, tracked: set[str]) -> bool:
    if "*" in ref:
        return any(fnmatch(path, ref) for path in tracked)
    if ref.endswith("/"):
        return any(path.startswith(ref) for path in tracked)
    return ref in tracked or any(path.startswith(ref.rstrip("/") + "/") for path in tracked)


def test_no_console_planning_docs() -> None:
    present = [rel for rel in FORBIDDEN_CONSOLE_DOCS if (REPO_ROOT / rel).exists()]
    assert present == [], f"console planning docs must not return: {present}"


def test_actor_model_is_surface_only() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in actors["entries"]}
    assert ids == CANONICAL_ACTOR_IDS, (
        f"actor set drifted from the four surfaces: {sorted(ids)}. "
        "A new actor requires a new execution surface (docs/DESIGN.md, Actor model)."
    )
    assert actors.get("actor_model_note"), "actors.json must keep the canonical actor_model_note"


def test_no_unsupported_gh_json_fields() -> None:
    offenders: list[str] = []
    for path in _markdown_files():
        for field_list in GH_JSON_PATTERN.findall(path.read_text(encoding="utf-8")):
            bad = FORBIDDEN_GH_JSON_FIELDS & set(field_list.split(","))
            if bad:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: {sorted(bad)}")
    assert offenders == [], f"unsupported gh --json fields found: {offenders}"


def test_canonical_command_bundle_source_normalized() -> None:
    assert (REPO_ROOT / "templates" / "pm-command-bundle.md").exists(), (
        "the single canonical command-bundle source must stay at templates/pm-command-bundle.md"
    )
    assert not (REPO_ROOT / "templates" / "commands").exists(), (
        "the single-file templates/commands/ folder was flattened; do not reintroduce it"
    )


def test_kernel_id_references_resolve_or_are_allowlisted() -> None:
    ids = _kernel_ids()
    offenders: list[str] = []
    for path in _tracked_text_files():
        rel = str(path.relative_to(REPO_ROOT))
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(path.read_text(encoding="utf-8")))):
            if (rel, ref) in KERNEL_ID_REFERENCE_ALLOWLIST:
                continue
            if "*" in ref:
                offenders.append(f"{rel}: pseudo kernel id {ref}")
            elif ref not in ids:
                offenders.append(f"{rel}: unresolved kernel id {ref}")
    assert offenders == [], f"kernel id reference drift found: {offenders}"


def test_no_role_actor_ids_in_durable_text() -> None:
    offenders: list[str] = []
    for path in _tracked_text_files():
        rel = str(path.relative_to(REPO_ROOT))
        for match in ROLE_ACTOR_ID_PATTERN.finditer(path.read_text(encoding="utf-8")):
            offenders.append(f"{rel}: {match.group(0)}")
    assert offenders == [], f"role-based actor ids found: {offenders}"


def test_positive_markdown_paths_resolve_or_are_allowlisted() -> None:
    tracked = _tracked_paths()
    offenders: list[str] = []
    for path in _markdown_files():
        rel = str(path.relative_to(REPO_ROOT))
        for token in sorted(set(MARKDOWN_PATH_PATTERN.findall(path.read_text(encoding="utf-8")))):
            ref = _normalize_markdown_path_ref(token)
            if ref is None or (rel, ref) in MARKDOWN_PATH_REFERENCE_ALLOWLIST:
                continue
            if not _tracked_ref_exists(ref, tracked):
                offenders.append(f"{rel}: {ref}")
    assert offenders == [], f"positive Markdown path references must resolve or be allowlisted: {offenders}"


def test_browser_activation_uses_kernel_owned_references() -> None:
    text = (REPO_ROOT / "adapters" / "BROWSER_CHAT.target.md").read_text(encoding="utf-8")
    block = text.split("~~~text", 1)[1].split("~~~", 1)[0]

    assert "kernel/manifest.json in REPOSITORY_NAME" not in block
    assert "mark the output pending" not in block
    assert "KERNEL_REPOSITORY's `kernel/manifest.json`" in block
    assert "KERNEL_REPOSITORY's `docs/TRACEABILITY_PROTOCOL.md`" in block
    assert "KERNEL_REPOSITORY's `templates/route-prompt.md`" in block
    assert re.search(r"KERNEL_REPOSITORY's\s+`templates/pm-command-bundle\.md`", block)
    assert "`status.needs_context`" in block


def test_review_before_close_requires_code_backed_kernel_evidence() -> None:
    boundary = _kernel_entry("boundaries.json", "boundary.review_before_close")
    workflow = _kernel_entry("workflows.json", "workflow.review_before_close")
    evidence = _kernel_entry("evidence.json", "evidence.pr_diff")
    review_output = _kernel_entry("outputs.json", "output.review_result")
    closure_output = _kernel_entry("outputs.json", "output.closure_comment")

    boundary_rule = boundary["rule"].lower()
    assert "linked issue objective, scope, out-of-scope, and acceptance criteria" in boundary_rule
    assert "pr body, comments, and reports are claims/evidence leads, not proof" in boundary_rule
    assert "code/diff/final-file evidence cannot be inspected" in boundary_rule
    assert "no closure comment is drafted" in boundary_rule

    workflow_steps = " ".join(workflow["steps"]).lower()
    assert "changed-file list" in workflow_steps
    assert "pr diff" in workflow_steps
    assert "relevant final head files" in workflow_steps
    assert "compare implementation behavior and validation" in workflow_steps
    assert "return status.needs_context instead of go" in workflow_steps

    pr_diff_rule = evidence["satisfied_by"].lower()
    assert "changed-file list and diff" in pr_diff_rule
    assert "final head file content" in pr_diff_rule
    assert "terminal-agent reports" in pr_diff_rule
    assert "not proof of implementation" in pr_diff_rule
    assert "status.needs_context instead of go" in pr_diff_rule

    assert (
        "implementation comparison mapping issue objective/scope/out-of-scope/acceptance criteria to code evidence"
        in review_output["required_sections"]
    )
    assert "documentation-only review" in review_output["rule"].lower()
    assert "not go" in review_output["rule"].lower()
    assert "draft it only after code-backed review" in closure_output["rule"].lower()


def test_review_before_close_route_template_rejects_documentation_only_go() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    review_variant = text.split("**Review a PR before merge/close**", 1)[1].split(
        "- **Apply review corrections**", 1
    )[0]
    compact = " ".join(review_variant.split())

    assert "PR body/comments/reports only as claims" in review_variant
    assert "inspect changed files, PR diff" in review_variant
    assert "relevant final head files" in review_variant
    assert "Compare implementation behavior against issue objective/scope/out-of-scope/acceptance" in compact
    assert "return `status.needs_context`, not GO" in review_variant
    assert "explicit not-reviewed gaps" in compact


def test_target_adoption_kernel_guards_audit_draft_and_bootstrap_paths() -> None:
    workflow = _kernel_entry("workflows.json", "workflow.target_adoption")
    evidence = _kernel_entry("evidence.json", "evidence.target_adoption")
    output = _kernel_entry("outputs.json", "output.adoption_packet")
    delegated_pr = _kernel_entry("execution_modes.json", "mode.delegated_commit_pr")

    steps = " ".join(workflow["steps"]).lower()
    assert workflow["required_evidence_refs"] == ["evidence.target_adoption"]
    assert "inspect target adoption state first" in steps
    assert "agents.md" in steps
    assert "claude.md" in steps
    assert "browser-chat adapter" in steps
    assert "audit them against kernel_repository adapters/*.target.md" in steps
    assert "tools.audit_target_adapters" in steps
    assert "protected overlay removal risk" in steps
    assert "without overwriting target-owned notes" in steps
    assert "mode.review_only" in steps
    assert "draft adapter content and checklist only" in steps
    assert "do not edit files or mutate git/github" in steps
    assert "mode.delegated_commit_pr" in steps
    assert "exact pm approval" in steps
    assert "create only agents.md and claude.md" in steps
    assert "adapter-only diff" in steps
    assert "no product code" in steps
    assert "secret-store authority" in steps

    evidence_text = evidence["satisfied_by"].lower()
    assert "agents.md/claude.md/browser-chat adapter presence" in evidence_text
    assert "project notes" in evidence_text
    assert "validation commands" in evidence_text
    assert "audit findings" in evidence_text

    assert "evidence.branch_preflight" in delegated_pr["required_evidence_refs"]
    assert "evidence.pm_approval" in delegated_pr["required_evidence_refs"]
    assert "evidence.validation_output" in delegated_pr["required_evidence_refs"]

    sections = output["required_sections"]
    assert "current adoption state" in sections
    assert "files missing/present" in sections
    assert "audit findings" in sections
    assert "exact write scope when applicable" in sections
    assert any("security/domain constraints" in section for section in sections)


def test_target_adoption_route_template_is_draft_or_adapter_only() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    variant = text.split("**Adopt target repository**", 1)[1].split(
        "- **Review a PR before merge/close**", 1
    )[0]
    compact = " ".join(variant.split())

    assert "`WORKFLOW = workflow.target_adoption`" in variant
    assert "`EXECUTION_MODE = mode.review_only | mode.delegated_commit_pr`" in variant
    assert "`EVIDENCE_REQUIRED = evidence.target_adoption` for review-only" in variant
    assert "evidence.branch_preflight" in variant
    assert "evidence.pm_approval" in variant
    assert "evidence.validation_output" in variant
    assert "for delegated_commit_pr" in variant
    assert "inspect TARGET_REPOSITORY first" in variant
    assert "whether `AGENTS.md` exists" in variant
    assert "whether `CLAUDE.md` exists" in variant
    assert "whether a browser-chat" in variant
    assert "adapter was supplied" in variant
    assert "audit/compare them against KERNEL_REPOSITORY's" in variant
    assert "`tools.audit_target_adapters`" in variant
    assert "preserve target-owned notes, security/domain constraints, and validation commands" in compact
    assert "review-only drafts only" in variant
    assert "may create only `AGENTS.md` and `CLAUDE.md`" in variant
    assert "open a draft PR" in compact
    assert "Browser chat remains draft-only" in variant
    assert "Do not merge, close, label" in variant
    assert "touch secrets" in variant


def test_artifact_templates_mark_review_claims_and_closure_precondition() -> None:
    text = (REPO_ROOT / "templates" / "artifacts.md").read_text(encoding="utf-8")
    pull_request = text.split("## Pull request", 1)[1].split("## Closure comment", 1)[0]
    closure_comment = text.split("## Closure comment", 1)[1].split("~~~markdown", 1)[0]

    assert "records claims and validation leads" in pull_request
    assert "not proof of implementation" in pull_request
    assert "changed files, PR diff, and relevant final head files" in pull_request

    assert "Draft this from `workflow.review_before_close` only after" in closure_comment
    assert "linked issue objective, scope, out-of-scope, and acceptance criteria" in closure_comment
    assert "PR changed files, diff, and relevant final head files" in closure_comment
    assert "claims/evidence leads, not proof" in closure_comment
