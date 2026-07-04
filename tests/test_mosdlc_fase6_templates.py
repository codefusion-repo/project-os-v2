"""MOSDLC.7 Fase 6 template migration guards."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_OPERATION_MAP.md"
STANDARD_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_TEMPLATE_STANDARD.md"
MOSDLC_FASE6_DIR = REPO_ROOT / "templates" / "mosdlc" / "operations" / "fase-6"
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
KERNEL_GROWTH_CANDIDATES = {
    ".".join(parts)
    for parts in (
        ("workflow", "deployment"),
        ("mode", "delegated_deploy_execution"),
        ("evidence", "deployment_readiness"),
        ("actor", "external_recipient"),
    )
}
FASE6_IDS = [f"MOS-6.{index}" for index in range(1, 13)]
ANALYSIS_ROWS = {"MOS-6.1", "MOS-6.2", "MOS-6.3", "MOS-6.4", "MOS-6.5", "MOS-6.6"}
PROCESSING_ROWS = {
    "MOS-6.7",
    "MOS-6.8",
    "MOS-6.9",
    "MOS-6.10",
    "MOS-6.11",
    "MOS-6.12",
}
REQUIRED_LEGACY_SOURCES = {"20", "25", "31"}

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
    in_fase6 = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_fase6 = line.strip().startswith("## Fase 6 ")
            headers = None
            continue
        if not in_fase6:
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
    return sorted(MOSDLC_FASE6_DIR.glob("MOS-6.*.md"), key=lambda path: _mosdlc_sort_key(path.stem))


def _template_path(row: dict[str, str]) -> Path:
    return MOSDLC_FASE6_DIR / f"{row['ID']}-{row['Operación']}.md"


def _legacy_refs(row: dict[str, str]) -> list[str]:
    legacy_paths = {
        path.name[:2]: f"templates/operations/{path.name}"
        for path in sorted(LEGACY_OPERATIONS_DIR.glob("*.md"))
    }
    refs: list[str] = []
    for number in re.findall(r"\b\d{2}\b", row["Mapa 00–37"]):
        ref = legacy_paths[number]
        if ref not in refs:
            refs.append(ref)
    return refs


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


def test_mosdlc_fase6_templates_are_documented_and_discoverable() -> None:
    rows = _parse_operation_rows()
    standard = STANDARD_DOC_PATH.read_text(encoding="utf-8")
    catalog = (REPO_ROOT / "docs" / "PM_OPERATIONS.md").read_text(encoding="utf-8")
    flows = (REPO_ROOT / "docs" / "OPERATION_FLOWS.md").read_text(encoding="utf-8")

    for fragment in (
        "## Fase 6 Migrada",
        "templates/mosdlc/operations/fase-6/",
        "El wizard local sigue leyendo `templates/operations/`",
        "Template authority: none",
    ):
        assert fragment in standard

    for rid, row in rows.items():
        path = f"templates/mosdlc/operations/fase-6/{rid}-{row['Operación']}.md"
        assert rid in standard
        assert path in standard
        assert path in catalog
        assert path in flows


def test_fase6_map_rows_have_matching_mosdlc_templates() -> None:
    rows = _parse_operation_rows()
    assert list(rows) == FASE6_IDS
    assert [path.name for path in _mosdlc_template_paths()] == [
        f"{rows[rid]['ID']}-{rows[rid]['Operación']}.md" for rid in FASE6_IDS
    ]

    for rid, row in rows.items():
        path = _template_path(row)
        text = path.read_text(encoding="utf-8")
        assert f"ID: {rid}" in text
        assert row["Operación"] in text
        for legacy in _legacy_refs(row):
            assert Path(legacy).name[:2] in row["Mapa 00–37"]
            assert legacy in text
        if not _legacy_refs(row):
            assert row["Mapa 00–37"] == "—"
            assert "Compatibility source: none" in text
        for block in REQUIRED_BLOCKS:
            assert block in text, f"{path.name} missing {block}"


def test_fase6_template_metadata_matches_source_map_kernel_contract() -> None:
    rows = _parse_operation_rows()
    for rid, row in rows.items():
        text = _template_path(row).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)

        assert metadata["ID"] == rid
        assert metadata["Classification"] == row["Clasificación"]
        assert metadata["Workflow"] == row["Workflow"]
        assert metadata["Mode"] == row["Mode"]
        assert row["Kernel/Template"].endswith("kernel:no-change")
        assert set(re.findall(r"output\.[A-Za-z0-9_]+", metadata["Output"])) == set(
            re.findall(r"output\.[A-Za-z0-9_]+", row["Output"])
        )
        assert set(re.findall(r"evidence\.[A-Za-z0-9_]+", metadata["Evidence"])) == set(
            re.findall(r"evidence\.[A-Za-z0-9_]+", row["Evidence"])
        )
        for legacy in _legacy_refs(row):
            assert legacy in metadata["Compatibility source"]


def test_fase6_templates_use_required_fields_and_optional_human_context() -> None:
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


def test_fase6_templates_reference_only_valid_kernel_ids() -> None:
    kernel_ids = _kernel_ids()
    offenders: list[str] = []
    for path in _mosdlc_template_paths() + [STANDARD_DOC_PATH]:
        text = path.read_text(encoding="utf-8")
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            if ref not in kernel_ids:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: invalid kernel id {ref}")
    assert offenders == []


def test_fase6_templates_do_not_store_live_state_or_authority_grants() -> None:
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


def test_fase6_analysis_rows_are_read_only_and_do_not_claim_completion() -> None:
    rows = _parse_operation_rows()
    for rid in ANALYSIS_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "Read-only" in text
        assert "status.needs_context" in text
        assert "output.status_result" in text


def test_fase6_processing_rows_are_non_authorizing_and_pm_executed() -> None:
    rows = _parse_operation_rows()
    for rid in PROCESSING_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        for fragment in (
            "PM decision",
            "only when evidence supports that route",
            "Draft-only classification",
            "non-authorizing outputs",
            "Human PM-executed",
        ):
            assert fragment in text, f"{rid} missing {fragment!r}"


def test_fase6_templates_do_not_imply_kernel_growth() -> None:
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8")
        for candidate in KERNEL_GROWTH_CANDIDATES:
            assert candidate not in text
        assert "kernel:no-change" not in text


def test_legacy_00_37_templates_remain_usable_and_fase6_sources_are_preserved() -> None:
    rows = _parse_operation_rows()
    expected = [f"{index:02d}" for index in range(38)]
    legacy_paths = sorted(LEGACY_OPERATIONS_DIR.glob("*.md"))
    assert [path.name[:2] for path in legacy_paths] == expected

    referenced_sources = {
        Path(legacy_ref).name[:2]
        for row in rows.values()
        for legacy_ref in _legacy_refs(row)
    }
    assert referenced_sources == REQUIRED_LEGACY_SOURCES

    for rid, row in rows.items():
        for legacy_ref in _legacy_refs(row):
            legacy = REPO_ROOT / legacy_ref
            assert legacy.exists(), f"{rid} compatibility source missing: {legacy_ref}"
            assert legacy.read_text(encoding="utf-8").startswith("#")


def test_mosdlc_fase6_migration_does_not_expand_kernel_or_unsupported_phases() -> None:
    changed_files = _changed_files()
    migration_changed = any(
        path.startswith("templates/mosdlc/operations/fase-6/") and "/MOS-R." not in path for path in changed_files
    )
    if not migration_changed:
        return
    assert not any(path.startswith("kernel/") for path in changed_files)
    assert not any(path.startswith("templates/operations/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-5/") and "/MOS-R." not in path for path in changed_files)
    assert not any("/MOS-R." in path for path in changed_files)
    assert all(
        path.startswith(
            (
                "docs/",
                "tests/",
                "templates/mosdlc/operations/fase-6/",
            )
        )
        for path in changed_files
    )
