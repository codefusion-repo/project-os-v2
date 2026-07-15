"""Spanish-adapter guards for the read-only target adoption auditor."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.audit_target_adapters import (
    Source,
    _canonical_roadmap_lines,
    _check_overlay_removals,
    audit_target_adapters,
)


REPO_ROOT = Path(__file__).resolve().parents[1]

LEGACY_GENERIC_POLICY = """Security / project constraints:
- Follow target-specific security practices; for web/API/user-facing changes,
  consider OWASP secure-coding risks such as auth, authorization, sessions,
  input validation, file uploads, redirects, dependency risk, and admin surfaces.
- Never print, paste, commit, upload, summarize, quote, or expose `.env`,
  `.env.*`, private keys, API tokens, OAuth/client secrets, database URLs,
  cookies, session tokens, JWTs, production credentials, payment-provider keys,
  SSH/GPG keys, CI secrets, or secret-looking values.
- Treat sensitive values as unsafe even in tests, logs, screenshots, shell output,
  GitHub comments, PR bodies, validation reports, and copied command output.
- Redact sensitive values as `[REDACTED]`; report only file paths, variable names,
  and risk type.
- Do not run broad environment/config dumps such as `env`, `printenv`, `set`,
  framework config dumps, or CI secret-context dumps unless the PM explicitly
  scopes a safe redacted diagnostic.
- Do not modify secret stores, rotate keys, change production credentials, edit
  deployment secrets, or touch payment/auth production settings without separate
  exact PM approval.
- Keep build commands, protected paths, domain constraints, and validation notes
  here when they are stable and target-owned; never store issue/PR/branch state,
  SHAs, review status, release status, or live validation results.
- Follow proportional validation from `project-os-es/docs/reglas.md` and
  `project-os-es/kernel/reglas-operativas.json`: run scoped required checks,
  draft PM-run commands when useful validation should remain PM-executed, and
  do not impose Project OS-specific tests or add tests by default unless the
  issue risk justifies them.
"""


def filled_spanish_adapter(target: Path) -> str:
    text = (REPO_ROOT / "project-os-es/adapters/AGENTS.target.md").read_text(encoding="utf-8")
    replacements = {
        "{{PLACEHOLDERS}}": "placeholders",
        "{{ORG/REPO}}": "example/target",
        "{{PROJECT_NAME}}": "target",
        "{{ruta absoluta al repo target}}": str(target),
        "{{ruta absoluta a project-os-v2/project-os-es/kernel}}": str(
            REPO_ROOT / "project-os-es/kernel"
        ),
        '{{version adoptada o "tracks latest"}}': "tracks latest",
        "{{#ROADMAP_ISSUE}}": "#274",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def filled_browser_adapter(target: Path) -> str:
    text = (REPO_ROOT / "project-os-es/adapters/BROWSER_CHAT.target.md").read_text(encoding="utf-8")
    replacements = {
        "{{PLACEHOLDERS}}": "placeholders",
        "{{ORG/REPO}}": "example/target",
        "{{PROJECT_NAME}}": "target",
        "{{ruta local si existe}}": str(target),
        "{{ruta a project-os-es/kernel si existe}}": str(REPO_ROOT / "project-os-es/kernel"),
        '{{version adoptada o "tracks latest"}}': "tracks latest",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def test_spanish_template_headings_and_project_os_es_kernel_path_are_accepted(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text(filled_spanish_adapter(tmp_path), encoding="utf-8")
    for name in ("CLAUDE.md", "GEMINI.md"):
        (tmp_path / name).write_text("Usa AGENTS.md para comportamiento del repositorio.\n", encoding="utf-8")

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    codes = {finding.code for finding in findings}

    assert "TAA-META-KERNEL-PATH" not in codes
    assert "TAA-ROADMAP-MISSING" not in codes
    assert "TAA-ROADMAP-DUPLICATE" not in codes


def test_browser_adapter_needs_no_roadmap_anchor_to_pass_the_target_audit(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text(filled_spanish_adapter(tmp_path), encoding="utf-8")
    for name in ("CLAUDE.md", "GEMINI.md"):
        (tmp_path / name).write_text("Usa AGENTS.md para comportamiento del repositorio.\n", encoding="utf-8")

    findings = audit_target_adapters(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert findings == []


def test_spanish_roadmap_anchor_wording_is_canonical() -> None:
    source = Source(
        "AGENTS.md",
        "## Estado vivo\nLee el roadmap canónico `#274` al momento de la tarea.\n",
    )
    assert _canonical_roadmap_lines(source, "example/target") == [
        (2, "Lee el roadmap canónico `#274` al momento de la tarea.", ["example/target#274"])
    ]


def test_spanish_canonical_sections_are_not_misclassified_as_target_overlay() -> None:
    base = Source(
        "AGENTS.md",
        "## Contrato\nTexto anterior.\n\n"
        "## Resolución del kernel\nRuta anterior.\n\n"
        "## Outputs y artefactos\nForma anterior.\n\n"
        "## Seguridad y validación\nValidación anterior.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Contrato\nTexto nuevo.\n\n"
        "## Resolución del kernel\nRuta nueva.\n\n"
        "## Outputs y artefactos\nForma nueva.\n\n"
        "## Seguridad y validación\nValidación nueva.\n",
    )

    assert _check_overlay_removals(base, head) == []


def test_compact_headings_allow_canonical_changes_while_preserving_target_notes() -> None:
    base = Source(
        "AGENTS.md",
        "## Identidad del repositorio\nMetadata anterior.\n\n"
        "## Resolución del kernel\nRuta anterior.\n\n"
        "## Evidencia viva\nEvidencia anterior.\n\n"
        "## Project-specific notes\nConservar este comando estable.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Identidad del repositorio\nMetadata compactada.\n\n"
        "## Resolución del kernel\nRuta compactada.\n\n"
        "## Evidencia viva\nEvidencia compactada.\n\n"
        "## Notas propias del target\nConservar este comando estable.\n",
    )

    assert _check_overlay_removals(base, head) == []


def test_real_compaction_discards_generic_policy_but_preserves_target_constraints() -> None:
    base = Source(
        "AGENTS.md",
        "## Project-specific notes\n"
        f"{LEGACY_GENERIC_POLICY}"
        "- Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "- Keep `config/ledger-policy.yml` as a protected path.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Notas propias del repositorio\n"
        "La política completa vive en `project-os-es/docs/reglas.md`.\n"
        "- Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "- Keep `config/ledger-policy.yml` as a protected path.\n",
    )

    assert _check_overlay_removals(base, head) == []


@pytest.mark.parametrize("validation_outcome", ("result", "results", "outcome", "outcomes"))
def test_real_compaction_discards_legacy_validation_outcome_variants(
    validation_outcome: str,
) -> None:
    legacy_policy = LEGACY_GENERIC_POLICY.replace(
        "live validation results",
        f"live validation {validation_outcome}",
    )
    base = Source(
        "AGENTS.md",
        "## Project-specific notes\n"
        f"{legacy_policy}"
        "- Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "- Keep `config/ledger-policy.yml` as a protected path.\n"
        "- Customer-ledger entries must remain immutable after settlement.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Notas propias del repositorio\n"
        "La política completa vive en `project-os-es/docs/reglas.md`.\n"
        "- Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "- Keep `config/ledger-policy.yml` as a protected path.\n"
        "- Customer-ledger entries must remain immutable after settlement.\n",
    )

    assert _check_overlay_removals(base, head) == []


@pytest.mark.parametrize(
    "target_owned_extension",
    (
        "Run `bin/verify-customer-ledger` before releasing ledger changes.",
        "Keep `config/ledger-policy.yml` as a protected path.",
        "Customer-ledger entries must remain immutable after settlement.",
    ),
)
def test_extended_legacy_validation_outcomes_remain_target_owned(
    target_owned_extension: str,
) -> None:
    unit = (
        "- Keep build commands, protected paths, domain constraints, and validation notes here "
        "when they are stable and target-owned; never store issue/PR/branch state, SHAs, review "
        "status, release status, or live validation outcomes. "
        f"{target_owned_extension}"
    )
    base = Source("AGENTS.md", f"## Project-specific notes\n{unit}\n")
    head = Source("AGENTS.md", "## Project-specific notes\n")

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == unit


def test_generic_phrase_extended_with_a_stable_command_is_not_discarded() -> None:
    unit = "- Follow target-specific security practices; run `bin/pci-check` before every payment release."
    base = Source("AGENTS.md", f"## Project-specific notes\n{unit}\n")
    head = Source("AGENTS.md", "## Project-specific notes\n")

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == unit


def test_generic_phrase_extended_with_a_protected_path_is_not_discarded() -> None:
    unit = "- Follow target-specific security practices; keep `config/payment-policy.yml` protected."
    base = Source("AGENTS.md", f"## Project-specific notes\n{unit}\n")
    head = Source("AGENTS.md", "## Project-specific notes\n")

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == unit


def test_generic_phrase_extended_with_a_security_constraint_is_not_discarded() -> None:
    unit = "- Follow target-specific security practices; payment releases require dual approval."
    base = Source("AGENTS.md", f"## Project-specific notes\n{unit}\n")
    head = Source("AGENTS.md", "## Project-specific notes\n")

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == unit


def test_target_owned_units_normalize_bullet_markers_and_whitespace() -> None:
    base = Source(
        "AGENTS.md",
        "## Project-specific notes\n- Run `bin/pci-check` before every payment release.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Project-specific notes\n*   Run `bin/pci-check` before every payment release.\n",
    )

    assert _check_overlay_removals(base, head) == []


def test_hermetic_compaction_preserves_target_owned_overlays_with_heading_aliases() -> None:
    base = Source(
        "AGENTS.md",
        "## Project-specific notes\n"
        f"{LEGACY_GENERIC_POLICY}"
        "- Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "- Keep `config/ledger-policy.yml` as a protected path.\n"
        "- Payment exports require dual approval before production release.\n"
        "- Customer-ledger entries must remain immutable after settlement.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Notas propias del repositorio\n"
        "La política completa vive en `project-os-es/docs/reglas.md`.\n"
        "*   Run `bin/verify-customer-ledger` before releasing ledger changes.\n"
        "*   Keep `config/ledger-policy.yml` as a protected path.\n"
        "*   Payment exports require dual approval before production release.\n"
        "*   Customer-ledger entries must remain immutable after settlement.\n",
    )

    assert _check_overlay_removals(base, head) == []


def test_compact_target_notes_report_an_individual_removed_constraint() -> None:
    base = Source(
        "AGENTS.md",
        "## Notas propias del target\n"
        "Mantener este path protegido.\n"
        "Mantener esta restricción de dominio.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Notas propias del target\nMantener este path protegido.\n",
    )

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == "Mantener esta restricción de dominio."


def test_compact_target_notes_do_not_silence_a_removed_stable_command() -> None:
    base = Source(
        "AGENTS.md",
        "## Notas propias del target\n"
        "- Ejecuta `bin/verify-customer-ledger` antes de publicar cambios de ledger.\n"
        "- Mantener esta restricción de dominio.\n",
    )
    head = Source(
        "AGENTS.md",
        "## Notas propias del target\nMantener esta restricción de dominio.\n",
    )

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-CONTENT-REMOVED"]
    assert findings[0].evidence == "- Ejecuta `bin/verify-customer-ledger` antes de publicar cambios de ledger."


def test_compact_target_notes_remain_protected_in_a_base_to_head_audit() -> None:
    base = Source(
        "BROWSER_CHAT.md",
        "## Resolución y evidencia\nTexto anterior.\n\n"
        "## Notas propias del target\nNo eliminar esta restricción de dominio.\n",
    )
    head = Source("BROWSER_CHAT.md", "## Resolución y evidencia\nTexto compactado.\n")

    findings = _check_overlay_removals(base, head)

    assert [finding.code for finding in findings] == ["TAA-OVERLAY-SECTION-REMOVED"]
    assert findings[0].evidence == "Notas propias del target"
