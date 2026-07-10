"""Spanish traceability and active protected-path guards."""

from __future__ import annotations

from tools.audit_traceability import (
    Comment,
    PullRequest,
    _is_protected_file,
    _multi_outcome_finding,
    linked_issue_numbers,
    parse_closure_packet,
)


def test_all_active_project_os_es_surfaces_are_protected() -> None:
    for path in (
        "project-os-es/kernel/manifest.json",
        "project-os-es/operaciones/fase-3/MOS-3.5.md",
        "project-os-es/templates/reporte-ejecucion.md",
        "project-os-es/adapters/AGENTS.target.md",
        "project-os-es/docs/reglas.md",
        "project-os-es/habilidades/arquitectura-backend.md",
    ):
        assert _is_protected_file(path), path

    assert not _is_protected_file("legacy-project-os/kernel/manifest.json")


def test_spanish_closure_template_aliases_parse_completely() -> None:
    comment = Comment(
        1,
        "pm",
        "## Evidencia de completitud\nHecho.\n"
        "## Evidencia de validacion\n`pytest` - 1 passed.\n"
        "## Excepciones aceptadas\nNinguna.\n"
        "## Limites preservados\nScope respetado.\n"
        "## Nota de friccion\nNinguna.\n"
        "## Referencias\nIssue y PR vivos.\n",
    )
    packet = parse_closure_packet(comment)

    assert packet is not None
    assert set(packet.sections) == {
        "completion_evidence",
        "validation_evidence",
        "accepted_exceptions",
        "boundaries_preserved",
        "friction_note",
        "references",
    }


def test_spanish_closing_directives_participate_in_multi_outcome_detection() -> None:
    pr = PullRequest(
        number=9,
        title="Correcciones",
        body="Resuelve #405.\nCierra #406.",
        state="open",
    )
    finding = _multi_outcome_finding("example/target", pr)

    assert finding is not None
    assert "multiple_closing_refs=#405,#406" in finding.evidence


def test_pr_self_reference_is_not_misread_as_linked_issue() -> None:
    pr = PullRequest(
        number=406,
        title="Correcciones de #405",
        body="PR #406; resuelve #405.",
        state="open",
    )
    assert linked_issue_numbers(pr) == {405}
