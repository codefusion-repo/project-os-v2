"""MOSDLC.8 accepted recommended operation template guards (#393)."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_DOC_PATH = REPO_ROOT / "legacy-project-os" / "docs" / "MOSDLC_OPERATION_MAP.md"
STANDARD_DOC_PATH = REPO_ROOT / "legacy-project-os" / "docs" / "MOSDLC_TEMPLATE_STANDARD.md"
MOSDLC_OPERATIONS_DIR = REPO_ROOT / "legacy-project-os" / "templates" / "mosdlc" / "operations"
LEGACY_OPERATIONS_DIR = REPO_ROOT / "legacy-project-os" / "templates" / "operations"

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
RECOMMENDED_IDS = [f"MOS-R.{index}" for index in range(1, 24)]
RECOMMENDED_PLACEMENT = {
    "MOS-R.1": "fase-2",
    "MOS-R.2": "cross-fase",
    "MOS-R.3": "cross-fase",
    "MOS-R.4": "cross-fase",
    "MOS-R.5": "fase-0",
    "MOS-R.6": "fase-2",
    "MOS-R.7": "fase-3",
    "MOS-R.8": "fase-3",
    "MOS-R.9": "fase-3",
    "MOS-R.10": "fase-0",
    "MOS-R.11": "fase-5",
    "MOS-R.12": "fase-5",
    "MOS-R.13": "fase-5",
    "MOS-R.14": "fase-5",
    "MOS-R.15": "fase-5",
    "MOS-R.16": "fase-5",
    "MOS-R.17": "fase-6",
    "MOS-R.18": "fase-6",
    "MOS-R.19": "fase-4",
    "MOS-R.20": "fase-4",
    "MOS-R.21": "fase-4",
    "MOS-R.22": "fase-3",
    "MOS-R.23": "fase-3",
}
CROSS_PHASE_RECOMMENDED_IDS = {"MOS-R.2", "MOS-R.3", "MOS-R.4"}
READ_ONLY_ROWS = {
    "MOS-R.2",
    "MOS-R.4",
    "MOS-R.5",
    "MOS-R.7",
    "MOS-R.9",
    "MOS-R.11",
    "MOS-R.13",
    "MOS-R.17",
    "MOS-R.18",
    "MOS-R.20",
    "MOS-R.22",
}
PROCESSING_ROWS = {"MOS-R.3", "MOS-R.8", "MOS-R.14", "MOS-R.16", "MOS-R.21"}
EXACT_APPROVAL_ROWS = {"MOS-R.1", "MOS-R.6", "MOS-R.10", "MOS-R.23"}
INTERNAL_ONLY_ROWS = {"MOS-R.12", "MOS-R.15"}
VALIDATION_CYCLE_ROWS = {"MOS-R.19", "MOS-R.20", "MOS-R.21"}
# Target-agnostic contract: no operation in the canonical recommended batch may
# be dogfood-only or exclusive to project-os-v2 / Project OS internal work.
PROJECT_EXCLUSIVE_TOKENS = ("dogfood", "codefusion", "project-os-v2", "project os")
# Validation-cycle wording must work for different target project types.
VALIDATION_SURFACE_FRAGMENTS = (
    "internal QA",
    "staging",
    "UAT",
    "TestFlight",
    "release candidate",
    "playtest",
    "pilot",
)
DECISION_CATEGORY_FRAGMENTS = (
    "missing-context",
    "choose-route",
    "approve-correction",
    "create-follow-up",
    "stop-no-op",
    "return-to-source",
    "need-more-evidence",
)

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
    for path in sorted((REPO_ROOT / "legacy-project-os" / "kernel").glob("*.json")):
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
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.strip().startswith("## Operaciones recomendadas aceptadas")
            headers = None
            continue
        if not in_section:
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
    paths: list[Path] = []
    for rid in RECOMMENDED_IDS:
        matches = sorted((MOSDLC_OPERATIONS_DIR / RECOMMENDED_PLACEMENT[rid]).glob(f"{rid}-*.md"))
        assert len(matches) == 1, f"{rid} must have exactly one MOSDLC template"
        paths.append(matches[0])
    return paths


def _template_path(row: dict[str, str]) -> Path:
    return MOSDLC_OPERATIONS_DIR / RECOMMENDED_PLACEMENT[row["ID"]] / f"{row['ID']}-{row['Operación']}.md"


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


def test_mosdlc_recommended_templates_are_documented_and_discoverable() -> None:
    rows = _parse_operation_rows()
    standard = STANDARD_DOC_PATH.read_text(encoding="utf-8")
    catalog = (REPO_ROOT / "legacy-project-os" / "docs" / "PM_OPERATIONS.md").read_text(encoding="utf-8")
    flows = (REPO_ROOT / "legacy-project-os" / "docs" / "OPERATION_FLOWS.md").read_text(encoding="utf-8")
    map_doc = MAP_DOC_PATH.read_text(encoding="utf-8")

    for fragment in (
        "## Operaciones Recomendadas Migradas",
        "templates/mosdlc/operations/cross-fase/",
        "templates/mosdlc/operations/fase-<n>/",
        "El wizard local sigue leyendo `templates/operations/`",
        "Template authority: none",
    ):
        assert fragment in standard

    assert "templates/mosdlc/operations/cross-fase/" in map_doc
    assert "templates/mosdlc/operations/recommended/" not in standard
    assert "templates/mosdlc/operations/recommended/" not in catalog
    assert "templates/mosdlc/operations/recommended/" not in flows
    assert "templates/mosdlc/operations/recommended/" not in map_doc
    assert not (MOSDLC_OPERATIONS_DIR / "recommended").exists()

    for rid, row in rows.items():
        path = _template_path(row).relative_to(REPO_ROOT / "legacy-project-os").as_posix()
        assert rid in standard
        assert path in standard
        assert path in catalog
        assert path in flows


def test_recommended_templates_have_phase_or_cross_phase_placement() -> None:
    rows = _parse_operation_rows()
    assert set(RECOMMENDED_PLACEMENT) == set(RECOMMENDED_IDS)
    assert {rid for rid, folder in RECOMMENDED_PLACEMENT.items() if folder == "cross-fase"} == (
        CROSS_PHASE_RECOMMENDED_IDS
    )
    for rid, row in rows.items():
        path = _template_path(row)
        assert path.exists()
        if rid in CROSS_PHASE_RECOMMENDED_IDS:
            assert path.parent.name == "cross-fase"
        else:
            assert re.fullmatch(r"fase-[0-6]", path.parent.name)


def test_recommended_map_rows_have_matching_mosdlc_templates() -> None:
    rows = _parse_operation_rows()
    assert list(rows) == RECOMMENDED_IDS
    assert [path.name for path in _mosdlc_template_paths()] == [
        f"{rows[rid]['ID']}-{rows[rid]['Operación']}.md" for rid in RECOMMENDED_IDS
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


def test_recommended_template_metadata_matches_source_map_kernel_contract() -> None:
    rows = _parse_operation_rows()
    for rid, row in rows.items():
        text = _template_path(row).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)

        assert metadata["ID"] == rid
        assert metadata["Classification"] == row["Clasificación"]
        assert metadata["Workflow"] == row["Workflow"]
        assert metadata["Mode"] == row["Mode"]
        assert "accepted-recommended" in metadata["Classification"]
        assert row["Kernel/Template"].endswith("kernel:no-change")
        assert set(re.findall(r"output\.[A-Za-z0-9_]+", metadata["Output"])) == set(
            re.findall(r"output\.[A-Za-z0-9_]+", row["Output"])
        )
        assert set(re.findall(r"evidence\.[A-Za-z0-9_]+", metadata["Evidence"])) == set(
            re.findall(r"evidence\.[A-Za-z0-9_]+", row["Evidence"])
        )
        for legacy in _legacy_refs(row):
            assert legacy in metadata["Compatibility source"]


def test_recommended_templates_use_required_fields_and_optional_human_context() -> None:
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


def test_recommended_templates_reference_only_valid_kernel_ids() -> None:
    kernel_ids = _kernel_ids()
    offenders: list[str] = []
    for path in _mosdlc_template_paths() + [STANDARD_DOC_PATH]:
        text = path.read_text(encoding="utf-8")
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            if ref not in kernel_ids:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: invalid kernel id {ref}")
    assert offenders == []


def test_recommended_templates_do_not_store_live_state_or_authority_grants() -> None:
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


def test_recommended_templates_are_target_agnostic() -> None:
    """No dogfood-only or project-os-v2-only operation enters the canonical batch."""
    rows = _parse_operation_rows()
    offenders: list[str] = []
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8").lower()
        for token in PROJECT_EXCLUSIVE_TOKENS:
            if token in text:
                offenders.append(f"{path.name}: project-exclusive wording {token!r}")
    # The map keeps the PM statements verbatim, but short names and generic
    # descriptions must not stay dogfood-specific.
    for rid, row in rows.items():
        for cell in ("Operación", "Descripción"):
            if "dogfood" in row[cell].lower():
                offenders.append(f"map {rid}: dogfood wording in {cell}")
    assert offenders == []


def test_validation_cycle_rows_cover_multiple_target_types_and_fail_closed() -> None:
    rows = _parse_operation_rows()
    for rid in VALIDATION_CYCLE_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        for fragment in VALIDATION_SURFACE_FRAGMENTS:
            assert fragment in text, f"{rid} missing validation surface wording {fragment!r}"
    for rid in ("MOS-R.19", "MOS-R.20"):
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "fail closed" in text.lower(), f"{rid} must fail closed without a validation surface"
        assert "status.needs_context" in text


def test_process_needs_pm_decision_has_clear_variables_and_decision_categories() -> None:
    rows = _parse_operation_rows()
    text = _template_path(rows["MOS-R.3"]).read_text(encoding="utf-8")
    for variable in ("DECISION_SOURCE", "DECISION_CONTEXT", "DECISION_QUESTION", "DECISION_OPTIONS"):
        assert f"{variable}=<{variable}>" in text, f"MOS-R.3 missing required variable {variable}"
    for fragment in DECISION_CATEGORY_FRAGMENTS:
        assert fragment in text, f"MOS-R.3 missing decision category {fragment!r}"
    # Compatibility with root Operation 36 stays explicit and non-authorizing.
    assert "templates/operations/36-process-needs-pm-decision.md" in text
    assert "ORIGINATING_OPERATION to DECISION_SOURCE" in text
    for fragment in (
        "no hidden workflow engine",
        "no auto-approval",
        "never infer approval",
        "return status.needs_pm_decision",
    ):
        assert fragment in text, f"MOS-R.3 missing non-authorizing fragment {fragment!r}"


def test_recommended_read_only_rows_are_read_only_and_fail_closed() -> None:
    rows = _parse_operation_rows()
    for rid in READ_ONLY_ROWS:
        row = rows[rid]
        assert row["Aprobación PM"].startswith("No (read-only)"), f"{rid} must stay read-only"
        text = _template_path(row).read_text(encoding="utf-8")
        assert "Read-only" in text
        assert "status.needs_context" in text
        assert "output.status_result" in text


def test_recommended_processing_rows_are_non_authorizing_and_pm_executed() -> None:
    rows = _parse_operation_rows()
    for rid in PROCESSING_ROWS:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        for fragment in (
            "PM decision",
            "Draft-only",
            "non-authorizing output",
            "Human PM-executed",
        ):
            assert fragment in text, f"{rid} missing {fragment!r}"


def test_recommended_exact_approval_rows_require_separate_exact_pm_approval() -> None:
    rows = _parse_operation_rows()
    for rid in EXACT_APPROVAL_ROWS:
        row = rows[rid]
        assert row["Aprobación PM"].startswith("Sí (exacta"), f"{rid} must require exact PM approval"
        text = _template_path(row).read_text(encoding="utf-8")
        assert "separate exact PM approval" in text, f"{rid} missing exact-approval wording"


def test_recommended_strict_security_rows_stay_redacted_and_secret_safe() -> None:
    rows = _parse_operation_rows()
    strict_ids = {rid for rid, row in rows.items() if "sec:strict" in row["Postura"]}
    assert strict_ids, "the map must keep strict security rows in the recommended batch"
    for rid in strict_ids:
        text = _template_path(rows[rid]).read_text(encoding="utf-8")
        assert "[REDACTED]" in text, f"{rid} must keep strict redaction wording"
        assert "secret" in text.lower(), f"{rid} must keep secret-safety wording"


def test_recommended_internal_only_rows_keep_conversion_and_target_owned_commands() -> None:
    rows = _parse_operation_rows()
    internal_ids = {rid for rid, row in rows.items() if row["Exposición"] == "internal-only"}
    assert internal_ids == INTERNAL_ONLY_ROWS
    for rid in internal_ids:
        row = rows[rid]
        assert "pre-release:convert" in row["Postura"], f"{rid} must convert before public release"
        text = _template_path(row).read_text(encoding="utf-8")
        for fragment in (
            "Internal-only exposure",
            "pre-release convert",
            "target-owned",
            "Human PM-executed",
            "templates/pm-command-bundle.md",
            "Fail closed",
        ):
            assert fragment in text, f"{rid} missing {fragment!r}"


def test_recommended_templates_do_not_imply_kernel_growth() -> None:
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8")
        for candidate in KERNEL_GROWTH_CANDIDATES:
            assert candidate not in text
        assert "kernel:no-change" not in text


def test_legacy_00_37_templates_remain_usable_and_recommended_sources_are_preserved() -> None:
    rows = _parse_operation_rows()
    expected = [f"{index:02d}" for index in range(38)]
    legacy_paths = sorted(LEGACY_OPERATIONS_DIR.glob("*.md"))
    assert [path.name[:2] for path in legacy_paths] == expected

    for rid, row in rows.items():
        for legacy_ref in _legacy_refs(row):
            legacy = REPO_ROOT / "legacy-project-os" / legacy_ref
            assert legacy.exists(), f"{rid} compatibility source missing: {legacy_ref}"
            assert legacy.read_text(encoding="utf-8").startswith("#")


def test_mosdlc_recommended_migration_does_not_expand_kernel_or_unrelated_surfaces() -> None:
    changed_files = _changed_files()
    migration_changed = any(
        path.startswith("templates/mosdlc/operations/cross-fase/")
        or re.match(r"templates/mosdlc/operations/fase-[0-6]/MOS-R\.", path)
        for path in changed_files
    )
    if not migration_changed:
        return
    assert not any(path.startswith("kernel/") for path in changed_files)
    assert not any(path.startswith("project-os-es/") for path in changed_files)
    assert not (MOSDLC_OPERATIONS_DIR / "recommended").exists()
    # Root Operation 36 is the only 00-37 template that #393 may touch, narrowly.
    assert all(
        path == "templates/operations/36-process-needs-pm-decision.md"
        for path in changed_files
        if path.startswith("templates/operations/")
    )
    assert all(
        path.startswith(
            (
                "docs/",
                "tests/",
                "templates/mosdlc/operations/cross-fase/",
                "templates/mosdlc/operations/fase-0/MOS-R.",
                "templates/mosdlc/operations/fase-2/MOS-R.",
                "templates/mosdlc/operations/fase-3/MOS-R.",
                "templates/mosdlc/operations/fase-4/MOS-R.",
                "templates/mosdlc/operations/fase-5/MOS-R.",
                "templates/mosdlc/operations/fase-6/MOS-R.",
                "templates/operations/36-process-needs-pm-decision.md",
            )
        )
        or (
            path.startswith("templates/mosdlc/operations/recommended/")
            and not (REPO_ROOT / path).exists()
        )
        for path in changed_files
    )
