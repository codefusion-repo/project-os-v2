"""Spanish-adapter guards for the read-only target adoption auditor."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.audit_target_adapters import (
    Source,
    _canonical_roadmap_lines,
    _check_overlay_removals,
    _emit_human,
    _emit_json,
    _resolve_metadata_path,
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


def filled_spanish_adapter(
    target: Path,
    *,
    target_path: str | None = None,
    kernel_path: str | None = None,
) -> str:
    text = (REPO_ROOT / "project-os-es/adapters/AGENTS.target.md").read_text(encoding="utf-8")
    replacements = {
        "{{PLACEHOLDERS}}": "placeholders",
        "{{ORG/REPO}}": "example/target",
        "{{PROJECT_NAME}}": "target",
        '{{version adoptada o "tracks latest"}}': "tracks latest",
        "{{#ROADMAP_ISSUE}}": "#274",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if target_path is not None:
        text = text.replace(
            "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT",
            f"REPOSITORY_LOCAL_PATH = {target_path}",
        )
    if kernel_path is not None:
        text = text.replace(
            "KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR",
            f"KERNEL_LOCAL_PATH = {kernel_path}",
        )
    return text


def write_terminal_adapters(target: Path, agents: str) -> None:
    (target / "AGENTS.md").write_text(agents, encoding="utf-8")
    for name in ("CLAUDE.md", "GEMINI.md"):
        (target / name).write_text(
            "Usa AGENTS.md para comportamiento del repositorio.\n", encoding="utf-8"
        )


def write_fake_kernel(
    root: Path,
    *,
    surface: str = "project-os-es",
    language: str = "es",
    manifest_text: str | None = None,
    with_manifest: bool = True,
    with_resolver: bool = True,
) -> Path:
    kernel = root / surface / "kernel"
    kernel.mkdir(parents=True)
    if with_manifest:
        payload = manifest_text
        if payload is None:
            payload = json.dumps(
                {
                    "manifest": [
                        {
                            "key": "manifest.kernel_es",
                            "language": language,
                            "active": True,
                        }
                    ]
                }
            )
        (kernel / "manifest.json").write_text(payload, encoding="utf-8")
    if with_resolver:
        resolver = root / "tools" / "project_os_resolve.py"
        resolver.parent.mkdir(parents=True)
        resolver.write_text("raise SystemExit(0)\n", encoding="utf-8")
    return kernel


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
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    codes = {finding.code for finding in findings}

    assert "TAA-META-KERNEL-PATH" not in codes
    assert "TAA-ROADMAP-MISSING" not in codes
    assert "TAA-ROADMAP-DUPLICATE" not in codes


def test_browser_adapter_needs_no_roadmap_anchor_to_pass_the_target_audit(tmp_path: Path) -> None:
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )

    findings = audit_target_adapters(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert findings == []


def test_canonical_portable_variables_resolve_exact_target_and_kernel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))

    assert audit_target_adapters(tmp_path, expected_repository="example/target") == []


def test_braced_canonical_variable_references_are_exact_and_supported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agents = filled_spanish_adapter(tmp_path)
    agents = agents.replace(
        "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT",
        "REPOSITORY_LOCAL_PATH = ${PROJECT_OS_TARGET_ROOT}",
    ).replace(
        "KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR",
        "KERNEL_LOCAL_PATH = ${PROJECT_OS_KERNEL_DIR}",
    )
    write_terminal_adapters(tmp_path, agents)
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))

    assert audit_target_adapters(tmp_path, expected_repository="example/target") == []


def test_canonical_variable_must_resolve_to_an_absolute_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", "relative-target")
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")

    assert any(
        finding.code == "TAA-META-LOCAL-PATH"
        and finding.severity == "error"
        and finding.evidence == "PROJECT_OS_TARGET_ROOT"
        for finding in findings
    )


@pytest.mark.parametrize("variable", ("PROJECT_OS_TARGET_ROOT", "PROJECT_OS_KERNEL_DIR"))
@pytest.mark.parametrize("value", (None, ""))
def test_missing_or_empty_canonical_variable_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    variable: str,
    value: str | None,
) -> None:
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))
    if value is None:
        monkeypatch.delenv(variable)
    else:
        monkeypatch.setenv(variable, value)

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")

    path_findings = [finding for finding in findings if finding.code.endswith("-PATH")]
    assert len(path_findings) == 1
    assert path_findings[0].severity == "error"
    assert path_findings[0].evidence == variable


@pytest.mark.parametrize(
    ("field", "value", "variable"),
    (
        ("REPOSITORY_LOCAL_PATH", "$ARBITRARY_TARGET", "ARBITRARY_TARGET"),
        ("REPOSITORY_LOCAL_PATH", "$PWD", "PWD"),
        ("REPOSITORY_LOCAL_PATH", "$PROJECT_OS_TARGET_ROOT/subdir", "PROJECT_OS_TARGET_ROOT"),
        ("KERNEL_LOCAL_PATH", "$PROJECT_OS_TARGET_ROOT", "PROJECT_OS_TARGET_ROOT"),
    ),
)
def test_non_allowlisted_or_non_exact_variable_reference_fails_closed_without_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: str,
    variable: str,
) -> None:
    private_value = tmp_path / "private-user-path"
    monkeypatch.setenv(variable, str(private_value))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))
    agents = filled_spanish_adapter(tmp_path).replace(
        f"{field} = ${'PROJECT_OS_TARGET_ROOT' if field == 'REPOSITORY_LOCAL_PATH' else 'PROJECT_OS_KERNEL_DIR'}",
        f"{field} = {value}",
    )
    write_terminal_adapters(tmp_path, agents)

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.severity == "error" and finding.evidence == variable for finding in findings)
    assert str(private_value) not in rendered


def test_target_variable_resolving_to_another_checkout_fails_without_disclosure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    other_checkout = tmp_path / "private-other-checkout"
    other_checkout.mkdir()
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(other_checkout))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-LOCAL-PATH" for finding in findings)
    assert str(other_checkout) not in rendered


def test_kernel_without_manifest_fails_without_disclosure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    empty_kernel = write_fake_kernel(tmp_path / "private-checkout", with_manifest=False)
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(empty_kernel))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-KERNEL-MANIFEST" for finding in findings)
    assert str(empty_kernel) not in rendered


@pytest.mark.parametrize("manifest_text", ("", "{"))
def test_invalid_kernel_manifest_fails_without_disclosure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    manifest_text: str,
) -> None:
    private_checkout = tmp_path / "private-checkout"
    kernel = write_fake_kernel(private_checkout, manifest_text=manifest_text)
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(kernel))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-KERNEL-IDENTITY" for finding in findings)
    assert str(private_checkout) not in rendered


def test_opposite_kernel_surface_fails_without_disclosure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    private_checkout = tmp_path / "private-checkout"
    kernel = write_fake_kernel(
        private_checkout,
        surface="project-os-en",
        language="en",
    )
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(kernel))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-KERNEL-SURFACE" for finding in findings)
    assert str(private_checkout) not in rendered


@pytest.mark.parametrize(
    "manifest_entry",
    (
        {"key": "manifest.unexpected", "language": "es", "active": True},
        {"key": "manifest.kernel_es", "language": "en", "active": True},
        {"key": "manifest.kernel_es", "language": "es", "active": False},
    ),
)
def test_kernel_manifest_identity_fields_are_exact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    manifest_entry: dict[str, object],
) -> None:
    private_checkout = tmp_path / "private-checkout"
    kernel = write_fake_kernel(
        private_checkout,
        manifest_text=json.dumps({"manifest": [manifest_entry]}),
    )
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(kernel))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-KERNEL-IDENTITY" for finding in findings)
    assert str(private_checkout) not in rendered


def test_kernel_checkout_without_canonical_resolver_fails_without_disclosure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    private_checkout = tmp_path / "private-checkout"
    kernel = write_fake_kernel(private_checkout, with_resolver=False)
    write_terminal_adapters(tmp_path, filled_spanish_adapter(tmp_path))
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(tmp_path))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(kernel))

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    rendered = "\n".join(finding.render() for finding in findings)

    assert any(finding.code == "TAA-META-KERNEL-RESOLVER" for finding in findings)
    assert str(private_checkout) not in rendered


def test_neutral_mount_is_a_valid_absolute_literal_shape() -> None:
    resolved, variable = _resolve_metadata_path("REPOSITORY_LOCAL_PATH", "/workspace/example")

    assert resolved == Path("/workspace/example")
    assert variable is None


def test_json_output_redacts_the_audited_checkout_and_expanded_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    private_target = tmp_path / "private-user-checkout"
    private_target.mkdir()
    write_terminal_adapters(private_target, filled_spanish_adapter(private_target))
    wrong_target = tmp_path / "private-wrong-checkout"
    wrong_target.mkdir()
    monkeypatch.setenv("PROJECT_OS_TARGET_ROOT", str(wrong_target))
    monkeypatch.setenv("PROJECT_OS_KERNEL_DIR", str(REPO_ROOT / "project-os-es/kernel"))
    findings = audit_target_adapters(private_target, expected_repository="example/target")

    _emit_json(private_target, "example/target", findings)
    output = capsys.readouterr().out

    assert '"schema_version": 2' in output
    assert str(private_target) not in output
    assert str(wrong_target) not in output
    assert "PROJECT_OS_TARGET_ROOT" in output


@pytest.mark.parametrize("metadata_error", ("duplicate", "order"))
def test_path_metadata_findings_redact_literal_values_in_human_and_json_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    metadata_error: str,
) -> None:
    private_literal = tmp_path / "private-user" / "target-checkout"
    agents = filled_spanish_adapter(
        tmp_path,
        target_path=str(tmp_path),
        kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
    )
    if metadata_error == "duplicate":
        agents = agents.replace(
            f"REPOSITORY_LOCAL_PATH = {tmp_path}",
            f"REPOSITORY_LOCAL_PATH = {tmp_path}\n"
            f"REPOSITORY_LOCAL_PATH = {private_literal}",
            1,
        )
        expected_code = "TAA-META-DUPLICATE"
    else:
        kernel_line = f"KERNEL_LOCAL_PATH = {REPO_ROOT / 'project-os-es/kernel'}"
        agents = agents.replace(kernel_line + "\n", "", 1)
        agents = agents.replace(
            "PM_FACING_LANGUAGE = es\n",
            f"KERNEL_LOCAL_PATH = {private_literal}\nPM_FACING_LANGUAGE = es\n",
            1,
        )
        expected_code = "TAA-META-ORDER"
    write_terminal_adapters(tmp_path, agents)

    findings = audit_target_adapters(tmp_path, expected_repository="example/target")
    assert any(finding.code == expected_code for finding in findings)

    _emit_human(findings)
    human_output = capsys.readouterr().out
    _emit_json(tmp_path, "example/target", findings)
    json_output = capsys.readouterr().out

    assert str(private_literal) not in human_output
    assert str(private_literal) not in json_output


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
