"""Canonical operation, alias compatibility, and duplicate-contract guards."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import tools.operation_catalog as operation_catalog
from tools.operation_catalog import (
    load_operation_sources,
    validate_bilingual_alias_parity,
    validate_operation_catalog,
)
from tools.operation_prompt_wizard import (
    canonical_operations,
    discover_operations,
    render_prompt,
    resolve_operation_selection,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SPANISH_OPERATIONS = REPO_ROOT / "project-os-es/operaciones"
ENGLISH_OPERATIONS = REPO_ROOT / "project-os-en/operations"


def _write_canonical(path: Path, code: str, identity: str, aliases: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""# {code} — Canonical

<!-- project-os-operation
canonical_code: {code}
operation_id: {identity}
aliases: {aliases}
deprecation: none
compatibility_reason: Compatibility is explicit when an alias exists.
-->

MOSDLC operation `{identity}` · Phase 0 · Risk: low.

- Surface: browser_chat
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.issue_scope
- PM approval: No

**Does:** Stable purpose.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO

**Deliver:** output.status_result.

**Connections:** Next: MOS-R.2. Recommended: MOS-R.2.
""",
        encoding="utf-8",
    )


def _write_alias(path: Path, code: str, canonical: str, extra: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""# {code} — Alias

<!-- project-os-operation
canonical_code: {canonical}
alias_of: {canonical}
deprecation: supported
compatibility_reason: Historical code resolves to the canonical prompt.
-->

Compatibility stub only.
{extra}
""",
        encoding="utf-8",
    )


def test_active_alias_metadata_and_bilingual_parity_have_no_findings() -> None:
    spanish = load_operation_sources(SPANISH_OPERATIONS)
    english = load_operation_sources(ENGLISH_OPERATIONS)

    assert validate_operation_catalog(spanish) == []
    assert validate_operation_catalog(english) == []
    assert validate_bilingual_alias_parity(spanish, english) == []

    for sources in (spanish, english):
        canonical = next(source for source in sources if source.code == "MOS-0.4")
        alias = next(source for source in sources if source.code == "MOS-R.10")
        assert canonical.metadata.aliases == ("MOS-R.10",)
        assert alias.metadata.alias_of == "MOS-0.4"
        assert alias.metadata.deprecation == "supported"
        assert "**Variables**" not in alias.text


def test_maintenance_shared_contract_keeps_machine_fields_neutral_and_localizes_prose() -> None:
    for operations_dir in (SPANISH_OPERATIONS, ENGLISH_OPERATIONS):
        sources = {item.code: item for item in load_operation_sources(operations_dir)}
        canonical = sources["MOS-6.13"]
        assert canonical.metadata.shared_contract == "maintenance-analysis"
        assert "- Kernel:" not in canonical.localized_text
        assert "INPUT:" not in canonical.localized_text
        assert "**Variables**" not in canonical.localized_text
        assert "- Kernel:" in canonical.text
        for code in ("MOS-6.3", "MOS-6.4", "MOS-6.5"):
            assert sources[code].metadata.shared_contract == "maintenance-analysis"
            assert "alias_of:" not in sources[code].localized_text


def test_shared_contract_references_and_connections_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    contracts = tmp_path / "operation-contracts"
    contracts.mkdir()
    monkeypatch.setattr(operation_catalog, "SHARED_CONTRACT_ROOT", contracts)
    unknown = tmp_path / "unknown"
    unknown.mkdir()
    (unknown / "MOS-6.13-test.md").write_text(
        "<!-- project-os-operation\nshared_contract: missing\n-->", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="cannot read shared operation contract"):
        load_operation_sources(unknown)

    descriptor = json.loads((REPO_ROOT / "operation-contracts/maintenance-analysis.json").read_text(encoding="utf-8"))
    descriptor["canonical"]["connections"] = ["MOS-9.99"]
    (contracts / "maintenance-analysis.json").write_text(json.dumps(descriptor), encoding="utf-8")
    findings = validate_operation_catalog(load_operation_sources(SPANISH_OPERATIONS))
    assert any(item.code == "OPS-022" and item.status == "status.blocked" for item in findings)


def test_alias_is_not_a_separate_outcome_but_resolves_by_code_filename_and_path() -> None:
    operations = discover_operations(SPANISH_OPERATIONS)
    canonical = resolve_operation_selection(operations, "MOS-0.4")
    alias = next(operation for operation in operations if operation.mos_code == "MOS-R.10")

    assert canonical is not None
    # The alias is never enumerated as its own canonical outcome, yet it resolves
    # by every handle to the canonical and copies no contract of its own.
    assert alias not in canonical_operations(operations)
    assert resolve_operation_selection(operations, "MOS-R.10") == alias
    assert resolve_operation_selection(operations, alias.filename) == alias
    assert resolve_operation_selection(operations, alias.relative_path) == alias
    assert alias.text == canonical.text
    assert alias.variables == canonical.variables


def test_alias_selection_renders_the_canonical_contract() -> None:
    operations = discover_operations(ENGLISH_OPERATIONS)
    alias = resolve_operation_selection(operations, "phase-0/MOS-R.10-update-target-adapters-catalog.md")
    canonical = resolve_operation_selection(operations, "MOS-0.4")

    assert alias is not None and canonical is not None
    rendered = render_prompt(alias, {"TARGET_REPOSITORY": "owner/repo"})

    assert "TARGET_REPOSITORY=owner/repo" in rendered
    # The alias renders the canonical variables, not a divergent contract.
    assert alias.variables == canonical.variables


def test_alias_guards_fail_closed_for_dangling_cycles_and_copied_contracts(tmp_path: Path) -> None:
    dangling_root = tmp_path / "dangling"
    _write_alias(dangling_root / "MOS-R.10-alias.md", "MOS-R.10", "MOS-0.4")
    dangling = validate_operation_catalog(load_operation_sources(dangling_root))
    assert any(item.code == "OPS-007" and item.status == "status.blocked" for item in dangling)

    cycle_root = tmp_path / "cycle"
    _write_alias(cycle_root / "MOS-R.10-alias.md", "MOS-R.10", "MOS-R.11")
    _write_alias(cycle_root / "MOS-R.11-alias.md", "MOS-R.11", "MOS-R.10")
    cycle = validate_operation_catalog(load_operation_sources(cycle_root))
    assert any(item.code == "OPS-008" and item.status == "status.blocked" for item in cycle)

    copied_root = tmp_path / "copied"
    _write_canonical(copied_root / "MOS-0.4-canonical.md", "MOS-0.4", "adoption", "MOS-R.10")
    _write_alias(
        copied_root / "MOS-R.10-alias.md",
        "MOS-R.10",
        "MOS-0.4",
        extra="\n**Variables**\n- Required: DIFFERENT_GATE",
    )
    copied = validate_operation_catalog(load_operation_sources(copied_root))
    assert any(item.code == "OPS-014" and item.status == "status.blocked" for item in copied)


def test_duplicate_identity_requires_pm_decision_and_is_never_auto_aliased(tmp_path: Path) -> None:
    _write_canonical(tmp_path / "MOS-9.1-first.md", "MOS-9.1", "same-outcome")
    _write_canonical(tmp_path / "MOS-9.2-second.md", "MOS-9.2", "same-outcome")
    second = tmp_path / "MOS-9.2-second.md"
    second.write_text(
        second.read_text(encoding="utf-8").replace("**Does:** Stable purpose.", "**Does:** Different incidental wording."),
        encoding="utf-8",
    )

    findings = validate_operation_catalog(load_operation_sources(tmp_path))

    assert any(item.code == "OPS-015" for item in findings)
    assert any(item.code == "OPS-016" for item in findings)
    assert all(
        item.status == "status.needs_pm_decision"
        for item in findings
        if item.code in {"OPS-015", "OPS-016"}
    )


def test_duplicate_contract_with_distinct_ids_and_wording_requires_pm_decision(
    tmp_path: Path,
) -> None:
    _write_canonical(tmp_path / "MOS-9.1-first.md", "MOS-9.1", "first-outcome")
    _write_canonical(tmp_path / "MOS-9.2-second.md", "MOS-9.2", "second-outcome")
    second = tmp_path / "MOS-9.2-second.md"
    second.write_text(
        second.read_text(encoding="utf-8").replace(
            "**Does:** Stable purpose.", "**Does:** Different incidental wording."
        ),
        encoding="utf-8",
    )

    sources = load_operation_sources(tmp_path)
    findings = validate_operation_catalog(sources)

    assert not any(item.code == "OPS-015" for item in findings)
    assert any(
        item.code == "OPS-016" and item.status == "status.needs_pm_decision"
        for item in findings
    )
    assert all(not source.is_alias for source in sources)


def test_material_contract_difference_avoids_duplicate_candidate(tmp_path: Path) -> None:
    _write_canonical(tmp_path / "MOS-9.1-first.md", "MOS-9.1", "first-outcome")
    _write_canonical(tmp_path / "MOS-9.2-second.md", "MOS-9.2", "second-outcome")
    second = tmp_path / "MOS-9.2-second.md"
    second.write_text(
        second.read_text(encoding="utf-8").replace(
            "output.status_result", "output.execution_report"
        ),
        encoding="utf-8",
    )

    assert validate_operation_catalog(load_operation_sources(tmp_path)) == []


def test_bilingual_alias_drift_is_blocking(tmp_path: Path) -> None:
    es = tmp_path / "es"
    en = tmp_path / "en"
    for root in (es, en):
        _write_canonical(root / "MOS-0.4-canonical.md", "MOS-0.4", "adoption", "MOS-R.10")
        _write_alias(root / "MOS-R.10-alias.md", "MOS-R.10", "MOS-0.4")
    en_alias = en / "MOS-R.10-alias.md"
    en_alias.write_text(
        en_alias.read_text(encoding="utf-8").replace("deprecation: supported", "deprecation: deprecated"),
        encoding="utf-8",
    )

    findings = validate_bilingual_alias_parity(
        load_operation_sources(es), load_operation_sources(en)
    )
    assert any(item.code == "OPS-018" and item.status == "status.blocked" for item in findings)


def test_alias_focus_area_must_be_allowlisted(tmp_path: Path) -> None:
    _write_canonical(tmp_path / "MOS-6.13-canonical.md", "MOS-6.13", "maintenance", "MOS-6.3")
    alias = tmp_path / "MOS-6.3-alias.md"
    _write_alias(alias, "MOS-6.3", "MOS-6.13")
    alias.write_text(
        alias.read_text(encoding="utf-8").replace(
            "deprecation: supported", "deprecation: supported\nalias_focus_area: mixed"
        ),
        encoding="utf-8",
    )

    findings = validate_operation_catalog(load_operation_sources(tmp_path))

    assert any(item.code == "OPS-020" and item.status == "status.blocked" for item in findings)


def test_alias_focus_area_requires_a_matching_canonical_input(tmp_path: Path) -> None:
    _write_canonical(tmp_path / "MOS-6.13-canonical.md", "MOS-6.13", "maintenance", "MOS-6.3")
    alias = tmp_path / "MOS-6.3-alias.md"
    _write_alias(alias, "MOS-6.3", "MOS-6.13")
    alias.write_text(
        alias.read_text(encoding="utf-8").replace(
            "deprecation: supported", "deprecation: supported\nalias_focus_area: performance"
        ),
        encoding="utf-8",
    )

    findings = validate_operation_catalog(load_operation_sources(tmp_path))

    assert any(item.code == "OPS-021" and item.status == "status.blocked" for item in findings)
