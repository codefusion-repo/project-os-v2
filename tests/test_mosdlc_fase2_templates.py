"""MOSDLC.3 Fase 2 template migration guards."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_OPERATION_MAP.md"
STANDARD_DOC_PATH = REPO_ROOT / "docs" / "MOSDLC_TEMPLATE_STANDARD.md"
MOSDLC_FASE2_DIR = REPO_ROOT / "templates" / "mosdlc" / "operations" / "fase-2"
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
    )
}

FASE2_ROWS = {
    "MOS-2.1": {
        "operation": "draft-architecture-diagrams",
        "template": "MOS-2.1-draft-architecture-diagrams.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.2": {
        "operation": "draft-uiux-docs",
        "template": "MOS-2.2-draft-uiux-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.3": {
        "operation": "draft-data-algorithms-docs",
        "template": "MOS-2.3-draft-data-algorithms-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.4": {
        "operation": "draft-coding-standards-docs",
        "template": "MOS-2.4-draft-coding-standards-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.5": {
        "operation": "draft-security-docs",
        "template": "MOS-2.5-draft-security-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.6": {
        "operation": "validate-design-docs",
        "template": "MOS-2.6-validate-design-docs.md",
        "legacy": [],
        "required": [],
        "optional": ["PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"],
    },
    "MOS-2.7": {
        "operation": "inventory-design-docs",
        "template": "MOS-2.7-inventory-design-docs.md",
        "legacy": [],
        "required": ["TARGET_REPOSITORY"],
        "optional": ["PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"],
    },
    "MOS-2.8": {
        "operation": "audit-design-doc-gaps",
        "template": "MOS-2.8-audit-design-doc-gaps.md",
        "legacy": ["templates/operations/05-review-project-state-and-misalignment.md"],
        "required": ["TARGET_REPOSITORY"],
        "optional": ["PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"],
    },
    "MOS-2.9": {
        "operation": "update-architecture-diagrams",
        "template": "MOS-2.9-update-architecture-diagrams.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.10": {
        "operation": "update-uiux-docs",
        "template": "MOS-2.10-update-uiux-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.11": {
        "operation": "update-data-algorithms-docs",
        "template": "MOS-2.11-update-data-algorithms-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.12": {
        "operation": "update-coding-standards-docs",
        "template": "MOS-2.12-update-coding-standards-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.13": {
        "operation": "update-security-docs",
        "template": "MOS-2.13-update-security-docs.md",
        "legacy": [
            "templates/operations/26-draft-docs-from-conversation.md",
            "templates/operations/28-draft-docs-from-description.md",
        ],
        "required": [],
        "optional": [
            "SOURCE_DOCS",
            "DOC_TARGET",
            "TARGET_REPOSITORY",
            "PM_FEEDBACK_HUMANO",
            "PM_QUESTION_HUMANO",
        ],
    },
    "MOS-2.14": {
        "operation": "validate-updated-design-docs",
        "template": "MOS-2.14-validate-updated-design-docs.md",
        "legacy": [],
        "required": [],
        "optional": ["PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"],
    },
}

DESIGN_WRITE_ROWS = {
    "MOS-2.1",
    "MOS-2.2",
    "MOS-2.3",
    "MOS-2.4",
    "MOS-2.5",
    "MOS-2.9",
    "MOS-2.10",
    "MOS-2.11",
    "MOS-2.12",
    "MOS-2.13",
}

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
    in_fase2 = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_fase2 = line.strip() == "## Fase 2 — Diseño"
            headers = None
            continue
        if not in_fase2:
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


def _mosdlc_template_paths() -> list[Path]:
    return sorted(MOSDLC_FASE2_DIR.glob("*.md"))


def test_mosdlc_fase2_templates_are_documented_and_discoverable() -> None:
    standard = STANDARD_DOC_PATH.read_text(encoding="utf-8")
    catalog = (REPO_ROOT / "docs" / "PM_OPERATIONS.md").read_text(encoding="utf-8")
    flows = (REPO_ROOT / "docs" / "OPERATION_FLOWS.md").read_text(encoding="utf-8")

    for fragment in (
        "## Fase 2 Migrada",
        "templates/mosdlc/operations/fase-2/",
        "El wizard local sigue leyendo `templates/operations/`",
        "Template authority: none",
    ):
        assert fragment in standard

    for rid, spec in FASE2_ROWS.items():
        path = f"templates/mosdlc/operations/fase-2/{spec['template']}"
        assert rid in standard
        assert path in standard
        assert path in catalog
        assert path in flows


def test_fase2_map_rows_have_matching_mosdlc_templates() -> None:
    rows = _parse_operation_rows()
    assert set(rows) == set(FASE2_ROWS)
    assert [path.name for path in _mosdlc_template_paths()] == [
        FASE2_ROWS[rid]["template"] for rid in sorted(FASE2_ROWS)
    ]

    for rid, spec in FASE2_ROWS.items():
        row = rows[rid]
        path = MOSDLC_FASE2_DIR / spec["template"]
        text = path.read_text(encoding="utf-8")
        assert row["Operación"] == spec["operation"]
        if spec["legacy"]:
            for legacy in spec["legacy"]:
                assert Path(legacy).name[:2] in row["Mapa 00–37"]
                assert legacy in text
        else:
            assert row["Mapa 00–37"] == "—"
            assert "Compatibility source: none" in text
        assert f"ID: {rid}" in text
        assert spec["operation"] in text
        for block in REQUIRED_BLOCKS:
            assert block in text, f"{path.name} missing {block}"


def test_fase2_template_metadata_matches_source_map_kernel_contract() -> None:
    rows = _parse_operation_rows()
    for rid, spec in FASE2_ROWS.items():
        row = rows[rid]
        text = (MOSDLC_FASE2_DIR / spec["template"]).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)

        assert metadata["ID"] == rid
        assert metadata["Classification"] == row["Clasificación"]
        assert metadata["Workflow"] == row["Workflow"]
        assert metadata["Mode"] == row["Mode"]
        assert set(re.findall(r"output\.[A-Za-z0-9_]+", metadata["Output"])) == set(
            re.findall(r"output\.[A-Za-z0-9_]+", row["Output"])
        )
        assert set(re.findall(r"evidence\.[A-Za-z0-9_]+", metadata["Evidence"])) == set(
            re.findall(r"evidence\.[A-Za-z0-9_]+", row["Evidence"])
        )
        for legacy in spec["legacy"]:
            assert legacy in metadata["Compatibility source"]


def test_fase2_templates_use_required_fields_and_optional_human_context() -> None:
    for rid, spec in FASE2_ROWS.items():
        path = MOSDLC_FASE2_DIR / spec["template"]
        text = path.read_text(encoding="utf-8")
        required, optional = _input_variables(text)

        assert required == spec["required"], f"{rid} required variables drifted"
        assert optional == spec["optional"], f"{rid} optional variables drifted"
        assert HUMAN_CONTEXT_VARIABLES.issubset(optional)
        assert HUMAN_CONTEXT_VARIABLES.isdisjoint(required)
        assert not LEGACY_PM_QUESTION_PATTERN.search(text)
        assert "PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only." in text


def test_fase2_templates_reference_only_valid_kernel_ids() -> None:
    kernel_ids = _kernel_ids()
    offenders: list[str] = []
    for path in _mosdlc_template_paths() + [STANDARD_DOC_PATH]:
        text = path.read_text(encoding="utf-8")
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            if ref not in kernel_ids:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: invalid kernel id {ref}")
    assert offenders == []


def test_fase2_design_write_flows_stay_route_prompt_gated() -> None:
    for rid in DESIGN_WRITE_ROWS:
        text = (MOSDLC_FASE2_DIR / FASE2_ROWS[rid]["template"]).read_text(encoding="utf-8")
        metadata = _mosdlc_metadata(text)
        assert metadata["Mode"] == "mode.review_only"
        assert "output.route_prompt" in metadata["Output"]
        assert "terminal writes require a separate route prompt and exact PM approval" in text
        assert "draft output.route_prompt with exact repository, path, scope, validation expectations, and PM authorization status" in text


def test_fase2_templates_do_not_store_live_state_or_authority_grants() -> None:
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


def test_fase2_templates_do_not_imply_kernel_growth() -> None:
    for path in _mosdlc_template_paths():
        text = path.read_text(encoding="utf-8")
        for candidate in KERNEL_GROWTH_CANDIDATES:
            assert candidate not in text
        assert "kernel:no-change" not in text


def test_legacy_00_37_templates_remain_usable_and_not_renumbered() -> None:
    expected = [f"{index:02d}" for index in range(38)]
    legacy_paths = sorted(LEGACY_OPERATIONS_DIR.glob("*.md"))
    assert [path.name[:2] for path in legacy_paths] == expected
    for rid, spec in FASE2_ROWS.items():
        for legacy_ref in spec["legacy"]:
            legacy = REPO_ROOT / legacy_ref
            assert legacy.exists(), f"{rid} compatibility source missing: {legacy_ref}"
            assert legacy.read_text(encoding="utf-8").startswith("#")


def test_mosdlc_fase2_migration_does_not_expand_kernel_or_unsupported_phases() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    changed_files = {line for line in changed.stdout.splitlines() if line}
    assert not any(path.startswith("kernel/") for path in changed_files)
    assert not any(path.startswith("templates/operations/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-3/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-4/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-5/") for path in changed_files)
    assert not any(path.startswith("templates/mosdlc/operations/fase-6/") for path in changed_files)
    assert not any("/MOS-R." in path for path in changed_files)
    assert all(
        path.startswith(
            (
                "docs/",
                "tests/",
                "templates/mosdlc/operations/fase-2/",
            )
        )
        for path in changed_files
    )
