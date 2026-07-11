"""Spanish-adapter guards for the read-only target adoption auditor."""

from __future__ import annotations

from pathlib import Path

from tools.audit_target_adapters import (
    Source,
    _canonical_roadmap_lines,
    _check_overlay_removals,
    audit_target_adapters,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


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
        "## Notas propias del target\nComando estable compactado.\n",
    )

    assert _check_overlay_removals(base, head) == []


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
