"""MOSDLC.6 Fase 5 template migration guards."""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_OPERATION_MAP.md"
STANDARD_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_TEMPLATE_STANDARD.md"
MOSDLC_FASE5_DIR = REPO_ROOT / "templates" / "mosdlc" / "operations" / "fase-5"
LEGACY_OPERATIONS_DIR = REPO_ROOT / "templates" / "operations"

HUMAN_CONTEXT_VARIABLES = {"PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"}
KERNEL_ID_PATTERN = re.compile(
    r"\b(?:status|actor|mode|boundary|evidence|workflow|output)\."
    r"(?!json\b|get\b|append\b)[A-Za-z0-9_*]+"
)
LIVE_GITHUB_OBJECT_PATTERN = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/(?:issues|pull)/\d+")
COMMIT_SHA_PATTERN = re.compile(
    r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b",
    re.IGNORECASE,
)
LEGACY_PM_QUESTION_PATTERN = re.compile(r"\bPM_QUESTION\b")
GH_JSON_PATTERN = re.compile(r"--json\s+([A-Za-z0-9_,]+)")
SUPPORTED_GH_JSON_FIELDS = {
    "state",
    "isDraft",
    "mergeable",
    "mergeStateStatus",
    "headRefName",
    "headRefOid",
    "mergedAt",
    "closedAt",
}
FORBIDDEN_GH_JSON_FIELDS = {"stateReason", "merged", "isLatest"}
SECRET_VALUE_PATTERNS = [
    re.compile(r"\b(?:TOKEN|SECRET|PASSWORD|DATABASE_URL|JWT|COOKIE|PRIVATE_KEY)\s*=\s*(?!<)", re.IGNORECASE),
    re.compile(r"\b(?:gho|ghp|sk|pk)_[A-Za-z0-9]{12,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]
KERNEL_GROWTH_CANDIDATES = {
    ".".join(parts)
    for parts in (
        ("workflow", "deployment"),
        ("mode", "delegated_deploy_execution"),
        ("evidence", "deployment_readiness"),
    )
}
FASE5_IDS = [f"MOS-5.{index}" for index in range(1, 16)]
READINESS_ROWS = {"MOS-5.1", "MOS-5.4", "MOS-5.7"}
CHECKLIST_ROWS = {"MOS-5.2", "MOS-5.5", "MOS-5.8"}
PROCESSING_ROWS = {"MOS-5.3", "MOS-5.6", "MOS-5.9"}
COMMAND_DRAFT_ROWS = {"MOS-5.10", "MOS-5.12", "MOS-5.14"}
EXECUTION_CANDIDATE_ROWS = {"MOS-5.11", "MOS-5.13", "MOS-5.15"}

REQUIRED_BLOCKS = [
    "MOSDLC:",
    "OPERATION:",
    "INPUT:",
    "KERNEL:",
    "COMPATIBILITY_SOURCE:",
    "LIVE_STATE:",
    "DO:",
    "OUTPUT:",
    "LIMITS:",
    "RECOMMENDED_NEXT_OPERATION:",
]


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


def _parse_operation_rows() -> dict[str, dict[str, str]]:
    text = MAP_DOC_PATH.read_text(encoding="utf-8")
    headers: list[str] | None = None
    rows: dict[str, dict[str, str]] = {}
    in_fase5 = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_fase5 = line.strip().startswith("## Fase 5 ")
            headers = None
            continue
        if not in_fase5:
            continue
        if line.startswith("| ID |"):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            continue
        if headers is not None and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            row = dict(zip(headers, cells, strict=True))
            rows[row["ID"]] = row
        elif headers is not None and not line.startswith("|"):
            break
    return rows


def _input_variables(text: str) -> tuple[list[str], list[str]]:
    match = re.search(r"INPUT:\n(.*?)(?:\n\n[A-Z_]+:|\Z)", text, re.DOTALL)
    assert match, "template has no INPUT block"
    required: list[str] = []
    optional: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line == "(none)":
            continue
        variable_match = re.search(r"([A-Z][A-Z0-9_]*)=", line)
        if not variable_match:
            continue
        target = optional if "# optional" in line else required
        target.append(variable_match.group(1))
    return required, optional


def _variables_from_map(cell: str) -> tuple[list[str], list[str]]:
    match = re.search(r"Req:\s*(.*?)\s*/\s*Opc:\s*(.*)", cell)
    assert match, f"cannot parse variable cell: {cell}"

    def split(raw: str) -> list[str]:
        if raw.strip() == "—":
            return []
        return [part.strip() for part in raw.split(",") if part.strip()]

    required = split(match.group(1))
    optional = split(match.group(2)) + sorted(HUMAN_CONTEXT_VARIABLES)
    return required, optional


def _mosdlc_metadata(text: str) -> dict[str, str]:
    match = re.search(r"MOSDLC:\n(.*?)(?:\n\n[A-Z_]+:|\Z)", text, re.DOTALL)
    assert match, "template has no MOSDLC metadata block"
    metadata: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def _mosdlc_sort_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", value))


def _mosdlc_template_paths() -> list[Path]:
    return sorted(MOSDLC_FASE5_DIR.glob("*.md"), key=lambda path: _mosdlc_sort_key(path.stem))


def _template_path(row: dict[str, str]) -> Path:
    return MOSDLC_FASE5_DIR / f"{row['ID']}-{row['Operación']}.md"


def _changed_files() -> set[str]:
    commands = (
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    changed: set[str] = set()
    for command in commands:
        proc = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        changed.update(line for line in proc.stdout.splitlines() if line)
    return changed


def _ascii_fold(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value) if not unicodedata.combining(char)
    )


def test_mosdlc_fase5_templates_are_documented_and_discoverable() -> None:
    rows = _parse_operation_rows()
    standard = STANDARD_DOC_PATH.read_text(encoding="utf-8")
    catalog = (REPO_ROOT / "docs" / "PM_OPERATIONS.md").read_text(encoding="utf-8")
    flows = (REPO_ROOT / "docs" / "OPERATION_FLOWS.md").read_text(encoding="utf-8")

    for fragment in (
        "## Fase 5 Migrada",
        "templates/mosdlc/operations/fase-5/",
        "MOS-5.11, MOS-5.13 y MOS-5.15",
        "preservan postura `kernel:candidate`",
        "El wizard local sigue leyendo `templates/operations/`",
        "Template authority: none",
    ):
        assert fragment in standard

    for rid, row in rows.items():
        path = f"templates/mosdlc/operations/fase-5/{rid}-{row['Operación']}.md"
        assert rid in standard
        assert path in standard
        assert path in catalog
        assert path in flows


def test_fase5_map_rows_have_matching_mosdlc_templates() -> None:
    rows = _parse_operation_rows()
    assert list(rows) == FASE5_IDS
    assert [path.name for path in _mosdlc_template_paths()] == [
        f"{rows[rid]['ID']}-{rows[rid]['Operación']}.md" for rid in FASE5_IDS
    ]

    for rid, row in rows.items():
        path = _template_path(row)
        text = path.read_text(encoding="utf-8")
        assert f"ID: {rid}" in text
        assert row["Operación"] in text
        assert row["Mapa 00–37"] == "—"
        assert "Compatibility source: none" in text
        for block in REQUIRED_BLOCKS:
            assert block in text, f"{path.name} missing {block}"


def test_fase5_template_metadata_matches_source_map_kernel_contract() -> None:
    rows = _parse_operation_rows()
    for rid, row in rows.items():
        text = _template_path(row).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)

        assert metadata["ID"] == rid
        assert _ascii_fold(metadata["Classification"]) == _ascii_fold(row["Clasificación"])
        if rid in EXECUTION_CANDIDATE_ROWS:
            assert "kernel:candidate" in row["Kernel/Template"]
            assert metadata["Workflow"].startswith("candidate")
            assert metadata["Mode"].startswith("candidate")
        else:
            assert metadata["Workflow"] == row["Workflow"]
            assert metadata["Mode"] == row["Mode"]
            assert row["Kernel/Template"].endswith("kernel:no-change")
        assert set(re.findall(r"output\.[A-Za-z0-9_]+", metadata["Output"])) == set(
            re.findall(r"output\.[A-Za-z0-9_]+", row["Output"])
        )
        assert set(re.findall(r"evidence\.[A-Za-z0-9_]+", metadata["Evidence"])) == set(
            re.findall(r"evidence\.[A-Za-z0-9_]+", row["Evidence"])
        )


def test_fase5_templates_use_required_fields_and_optional_human_context() -> None:
    rows = _parse_operation_rows()
    for rid, row in rows.items():
        text = _template_path(row).read_text(encoding="utf-8")
        required, optional = _input_variables(text)
        expected_required, expected_optional = _variables_from_map(row["Variables"])

        assert required == expected_required, f"{rid} required variables drifted"
        assert optional == expected_optional, f"{rid} optional variables drifted"
        assert HUMAN_CONTEXT_VARIABLES.issubset(optional)
        assert HUMAN_CONTEXT_VARIABLES.isdisjoint(required)
        assert not LEGACY_PM_QUESTION_PATTERN.search(text)
        assert "PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only." in text


def test_fase5_templates_reference_only_valid_kernel_ids_or_candidate_posture() -> None:
    kernel_ids = _kernel_ids()
    offenders: list[str] = []
    for path in _mosdlc_template_paths() + [STANDARD_DOC_PATH]:
        text = path.read_text(encoding="utf-8")
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            if ref not in kernel_ids:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: invalid kernel id {ref}")
    assert offenders == []

    rows = _parse_operation_rows()
    for rid in EXECUTION_CANDIDATE_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)
        assert metadata["Workflow"].startswith("candidate")
        assert metadata["Mode"].startswith("candidate")
        assert "Candidate posture only" in text
        assert "Use no new kernel ids" in text
        assert "fail-closed candidate-only" in text


def test_fase5_templates_do_not_store_live_state_or_authority_grants() -> None:
    offenders: list[str] = []
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8")
        if LIVE_GITHUB_OBJECT_PATTERN.search(text):
            offenders.append(f"{path.name}: durable live GitHub object URL")
        if re.search(r"\bwork/[0-9][A-Za-z0-9._/-]*\b", text):
            offenders.append(f"{path.name}: concrete work branch")
        if COMMIT_SHA_PATTERN.search(text):
            offenders.append(f"{path.name}: commit SHA")
        if re.search(r"\b(?:result|resultado):\s*(?:pass|passed|fail|failed)\b", text, re.IGNORECASE):
            offenders.append(f"{path.name}: validation result state")
        assert "Template authority: none." in text, f"{path.name} must deny template authority"
        assert "Exact PM approval plus kernel gates are required" in text
        assert "Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files." in text
    assert offenders == []


def test_fase5_secret_safety_and_no_deploy_authority_are_explicit() -> None:
    rows = _parse_operation_rows()
    for rid, row in rows.items():
        text = _template_path(row).read_text(encoding="utf-8")
        assert "[REDACTED]" in text
        assert "variable names" in text or "variable name" in text
        assert "risk types" in text or "risk type" in text
        assert "broad environment/config dumps" in text
        assert (
            "request secrets" in text
            or "request secret values" in text
            or "must never be requested" in text
        )
        assert (
            "no deployment" in text
            or "Do not execute" in text
            or "does not execute" in text
            or "Do not run" in text
        )
        for pattern in SECRET_VALUE_PATTERNS:
            assert not pattern.search(text), f"{rid} contains secret-looking value"


def test_fase5_readiness_checklists_and_processors_preserve_deployment_boundaries() -> None:
    rows = _parse_operation_rows()

    for rid in READINESS_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "Read-only/draft-only" in text
        assert "does not authorize" in text
        assert "Do not run" in text
        assert "deploy commands" in text

    for rid in CHECKLIST_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "Human PM-facing" in text
        assert "Human PM decides and performs" in text
        assert "values stay [REDACTED]" in text
        assert "Do not execute commands" in text

    for rid in PROCESSING_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        for fragment in (
            "continue",
            "correction",
            "follow-up",
            "no-op",
            "PM decision",
            "only when evidence supports that route",
        ):
            assert fragment in text
        assert "route prompts are non-authorizing outputs" in text
        assert "Human PM-executed" in text
        assert "Do not execute deployment" in text


def test_fase5_command_drafts_are_pm_executed_target_owned_and_gh_json_safe() -> None:
    rows = _parse_operation_rows()
    for rid in COMMAND_DRAFT_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "Human PM-executed" in text
        assert "target-owned" in text
        assert "Fail closed to status.needs_context" in text
        assert "Do not execute the bundle" in text
        assert "invent commands" in text
        assert "templates/pm-command-bundle.md" in text
        for field_list in GH_JSON_PATTERN.findall(text):
            fields = set(field_list.split(","))
            assert fields <= SUPPORTED_GH_JSON_FIELDS
            assert fields.isdisjoint(FORBIDDEN_GH_JSON_FIELDS)


def test_fase5_execution_rows_are_fail_closed_candidates_only() -> None:
    rows = _parse_operation_rows()
    for rid in EXECUTION_CANDIDATE_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "kernel:candidate" in rows[rid]["Kernel/Template"]
        assert "Candidate template only" in text
        assert "no deploy execution" in text
        assert "Do not execute" in text
        assert "Exact PM deploy approval alone does not convert" in text
        assert "Human PM" in text
        assert "Use no new kernel ids" in text


def test_fase5_templates_do_not_imply_kernel_growth_or_unsupported_phase_migration() -> None:
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8")
        for candidate in KERNEL_GROWTH_CANDIDATES:
            assert candidate not in text
        assert "kernel:no-change" not in text

    changed_files = _changed_files()
    migration_changed = any(path.startswith("templates/mosdlc/operations/fase-5/") for path in changed_files)
    if not migration_changed:
        return
    assert not any(path.startswith("kernel/") for path in changed_files)
    assert not any(path.startswith("templates/operations/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-6/") for path in changed_files)
    assert not any("/MOS-R." in path for path in changed_files)
    assert all(
        path.startswith(
            (
                "docs/",
                "tests/",
                "templates/mosdlc/operations/fase-5/",
            )
        )
        for path in changed_files
    )


def test_legacy_00_37_templates_remain_usable_and_unmodified() -> None:
    expected = [f"{index:02d}" for index in range(38)]
    legacy_paths = sorted(LEGACY_OPERATIONS_DIR.glob("*.md"))
    assert [path.name[:2] for path in legacy_paths] == expected
    for path in legacy_paths:
        assert path.read_text(encoding="utf-8").startswith("#")

    changed_files = _changed_files()
    assert not any(path.startswith("templates/operations/") for path in changed_files)
