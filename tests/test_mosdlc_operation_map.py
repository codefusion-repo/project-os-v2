"""MOSDLC.0 operation map guards.

These tests protect the durable MOSDLC mapping artifact
(docs/MOSDLC_OPERATION_MAP.md): every PM-written operation from the MOSDLC
roadmap comment on #274 is preserved verbatim, every accepted recommended
operation is mapped, deploy-by-agent operations stay internal-only and
secret-safe, the legacy 00-37 catalog is fully classified, and kernel-change
candidates are identified without being applied.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_DOC_PATH = REPO_ROOT / "legacy-project-os" / "docs" / "MOSDLC_OPERATION_MAP.md"

# Verbatim PM-written operations from the MOSDLC roadmap comment on #274.
# Preservation contract: every wording below must appear unchanged in the map.
PM_WRITTEN_OPERATIONS: dict[str, list[str]] = {
    "Fase 0": [
        "Activar Chat Browser y crear una sesión.",
        "Iniciar proyecto: iniciar un nuevo proyecto.",
        "Adoptar proyecto: adoptar un proyecto existente.",
        "Actualizar la adopción de un proyecto.",
        "Verificar la adopción del proyecto target.",
        "Transferir contexto de sesión.",
    ],
    "Fase 1": [
        "Identificar requisitos mediante entrevista.",
        "Resumir los requisitos identificados.",
        "Verificar la viabilidad de los requisitos identificados.",
        "Crear documentación de requisitos funcionales y no funcionales, casos de uso e historias de usuario.",
        "Validar la documentación creada.",
        "Planificar el roadmap general del proyecto.",
        "Revisar la viabilidad de una idea como nuevo requerimiento.",
        "Actualizar la documentación y el roadmap con el nuevo requerimiento.",
        "Revisar la eliminación de un requerimiento del proyecto.",
        "Identificar requisitos desde un proyecto existente.",
        "Actualizar o crear documentación de requisitos funcionales y no funcionales, casos de uso e historias de usuario para un proyecto existente.",
        "Actualizar o planificar el roadmap general del proyecto existente.",
    ],
    "Fase 2": [
        "Crear diagramas de arquitectura.",
        "Crear documentación de diseño UI/UX.",
        "Crear documentación de estructura de datos y algoritmos.",
        "Crear documentación de estándares de codificación.",
        "Crear documentación de seguridad basada en OWASP y en los 8 dominios de seguridad.",
        "Validar la documentación con respecto a la Fase 1.",
        "Identificar documentación de diseño existente.",
        "Identificar gaps en la documentación existente con respecto a la Fase 1.",
        "Actualizar o crear diagramas de arquitectura desde la documentación existente y la Fase 1.",
        "Actualizar o crear documentación de diseño UI/UX desde la documentación existente y la Fase 1.",
        "Actualizar o crear documentación de estructura de datos y algoritmos.",
        "Actualizar o crear documentación de estándares de codificación.",
        "Actualizar o crear documentación de seguridad basada en OWASP y en los 8 dominios de seguridad.",
        "Validar la documentación con respecto a la documentación existente y la Fase 1.",
    ],
    "Fase 3": [
        "Crear un issue desde trazabilidad viva y roadmap.",
        "Crear un conjunto de issues desde trazabilidad viva y roadmap.",
        "Crear un issue de follow-up desde un issue incompleto.",
        "Draftear un prompt para implementar un issue.",
        "Draftear un prompt de corrección de un PR/issue.",
        "Draftear comandos de cierre y limpieza para issue/PR.",
        "Revisar issue/PR antes de draftear comandos de cierre y limpieza.",
        "Draftear un issue desde una descripción y verificar que no afecte al roadmap ni a la documentación.",
        "Verificar el estado post-merge.",
        "Analizar la preparación de release-on-tag y draftear comandos de creación si está listo.",
        "Draftear comandos de creación de tag en GitHub.",
        "Draftear comandos de creación de release en GitHub.",
        "Auditar issue/PR y trazabilidad viva en GitHub.",
        "Procesar auditoría de issue/PR y trazabilidad viva.",
        "Solicitar asset 2D.",
        "Solicitar asset 3D.",
        "Solicitar asset de audio.",
        "Solicitar asset de video.",
        "Procesar entrega de asset 2D.",
        "Procesar entrega de asset 3D.",
        "Procesar entrega de asset de audio.",
        "Procesar entrega de asset de video.",
        "Solicitar revisión de seguridad OWASP y de los 8 dominios de seguridad donde corresponda.",
        "Auditar gaps en la disciplina de implementación.",
        "Procesar revisión de seguridad.",
        "Procesar auditoría de gaps de disciplina.",
        "Revisar el estado del proyecto y desalineaciones con respecto a la documentación.",
        "Draftear follow-up desde la auditoría de gaps.",
        "Draftear follow-up desde la revisión de seguridad.",
        "Draftear paso a paso de implementación manual de un issue.",
        "Procesar paso a paso de implementación manual.",
    ],
    "Fase 4": [
        "QA enfocado en checklist humano de issue/PR.",
        "QA enfocado en checklist humano de descripción.",
        "QA de production readiness con checklist humano.",
        "Procesar checklist humano de issue/PR.",
        "Procesar checklist humano de descripción/feature.",
        "Procesar checklist humano de production readiness.",
        "Draftear follow-up desde QA.",
        "Draftear prompt de corrección desde QA.",
    ],
    "Fase 5": [
        "Analizar y configurar despliegue local.",
        "Draftear checklist de despliegue local para los pasos humanos (.env, DB, etc.).",
        "Procesar pasos humanos de despliegue local.",
        "Analizar y configurar despliegue staging.",
        "Draftear checklist de despliegue staging para los pasos humanos: host, DNS, dashboards externos, etc.",
        "Procesar pasos humanos de despliegue staging.",
        "Analizar y configurar despliegue de producción.",
        "Draftear checklist de despliegue de producción para los pasos humanos.",
        "Procesar pasos humanos de despliegue de producción.",
        "Draftear comandos de despliegue local.",
        "Desplegar de manera local/debug, solo si es posible.",
        "Draftear comandos de despliegue staging.",
        "Desplegar en staging, solo si es posible.",
        "Draftear comandos de despliegue de producción.",
        "Desplegar en producción, solo si es posible.",
    ],
    "Fase 6": [
        "Revisar seguridad para production readiness.",
        "Revisar gaps de funcionalidades para production readiness.",
        "Analizar y recomendar mejoras de rendimiento.",
        "Analizar y recomendar mejoras de producto.",
        "Analizar y recomendar mejoras de normalización de código o gaps de clean code.",
        "Analizar en busca de código huérfano, código legacy, variables sin uso, funciones obsoletas y código inútil.",
        "Procesar resultados de seguridad para production readiness.",
        "Procesar resultados de gaps funcionales del sistema para production readiness.",
        "Procesar mejoras de rendimiento.",
        "Procesar mejoras de producto.",
        "Procesar mejoras de código.",
        "Procesar limpieza de código inútil.",
    ],
}

# Verbatim accepted recommended operations from issue scope.
ACCEPTED_RECOMMENDED_OPERATIONS: list[str] = [
    "record ADR decision",
    "recommend next operation",
    "process `status.needs_pm_decision`",
    "review phase readiness",
    "audit target adoption in batch",
    "create/update ADR from design or requirements",
    "review licensing/publication readiness",
    "process incident or hotfix",
    "audit drift between documentation and product",
    "update target adapters for a new catalog/kernel version",
    "deployment readiness review",
    "draft deployment command bundle",
    "post-deploy verification",
    "process deployment result",
    "rollback drafting",
    "process rollback result",
    "dependency/security-update audit",
    "secret-safe environment/config audit that reports only file paths, variable names, and risk types, never values",
    "plan internal dogfood cycle",
    "review dogfood readiness",
    "process dogfood findings into follow-ups",
    "public packaging safety review",
    "remove, hide, or convert internal-only operations before public release",
]

# Deployment requirements from the issue's deployment-by-agent decision, each
# of which must be mapped to a concrete row.
DEPLOYMENT_DECISION_REQUIREMENTS: list[str] = [
    "analyze local deployment readiness",
    "draft local deployment human checklist",
    "process local deployment checklist",
    "draft local deploy/debug commands",
    "execute local deploy/debug by terminal agent",
    "analyze staging deployment readiness",
    "draft staging deployment human checklist",
    "process staging deployment checklist",
    "draft staging deploy commands",
    "execute staging deploy by terminal agent",
    "analyze production deployment readiness",
    "draft production deployment human checklist",
    "process production deployment checklist",
    "draft production deploy commands",
    "execute production deploy by terminal agent",
    "verify post-deploy state",
    "process deployment result",
    "draft rollback commands or rollback route when deploy fails",
    "process rollback result",
]

PHASE_ROW_PREFIXES = {
    "Fase 0": "MOS-0.",
    "Fase 1": "MOS-1.",
    "Fase 2": "MOS-2.",
    "Fase 3": "MOS-3.",
    "Fase 4": "MOS-4.",
    "Fase 5": "MOS-5.",
    "Fase 6": "MOS-6.",
}
RECOMMENDED_ROW_PREFIX = "MOS-R."

# Kernel-change candidates the map may name; they must NOT exist in the kernel
# (identified only, never applied by this issue).
KERNEL_CHANGE_CANDIDATE_IDS = {
    "workflow.deployment",
    "mode.delegated_deploy_execution",
    "evidence.deployment_readiness",
}

DEPLOY_EXECUTE_ROW_IDS = {"MOS-5.11", "MOS-5.13", "MOS-5.15"}
INTERNAL_ONLY_ROW_IDS = {
    "MOS-5.10",
    "MOS-5.11",
    "MOS-5.12",
    "MOS-5.13",
    "MOS-5.14",
    "MOS-5.15",
    "MOS-R.12",
    "MOS-R.15",
}

CLASSIFICATION_TOKENS = {
    "new",
    "replacement",
    "alias",
    "variant",
    "merge-candidate",
    "split-candidate",
    "old-compatibility-reference",
    "accepted-recommended",
}
LEGACY_STATE_TOKENS = {"replacement-source", "compatibility-reference"}
RISK_TOKENS = {"low", "medium", "high"}
EXPOSURE_TOKENS = {"public-safe", "internal-only"}

KERNEL_ID_PATTERN = re.compile(
    r"\b(?:status|actor|mode|boundary|evidence|workflow|output)\."
    r"(?!json\b)[A-Za-z0-9_]+"
)


def _doc_text() -> str:
    assert MAP_DOC_PATH.exists(), "docs/MOSDLC_OPERATION_MAP.md must exist"
    return MAP_DOC_PATH.read_text(encoding="utf-8")


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


def _parse_tables(text: str, header_first_cell: str) -> dict[str, list[dict[str, str]]]:
    """Return section-heading -> rows for tables whose header starts with the cell."""
    sections: dict[str, list[dict[str, str]]] = {}
    current_heading = ""
    headers: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("#"):
            current_heading = line.lstrip("#").strip()
            headers = None
            continue
        if line.startswith(f"| {header_first_cell} |"):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            sections.setdefault(current_heading, [])
            continue
        if headers is not None and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            assert len(cells) == len(headers), f"malformed row under {current_heading}: {line}"
            sections[current_heading].append(dict(zip(headers, cells, strict=True)))
        elif headers is not None and not line.startswith("|"):
            headers = None
    return sections


def _operation_rows() -> dict[str, list[dict[str, str]]]:
    return _parse_tables(_doc_text(), "ID")


def _all_rows() -> list[dict[str, str]]:
    return [row for rows in _operation_rows().values() for row in rows]


def _rows_by_id() -> dict[str, dict[str, str]]:
    rows = {}
    for row in _all_rows():
        assert row["ID"] not in rows, f"duplicated map row id {row['ID']}"
        rows[row["ID"]] = row
    return rows


def _section_rows(prefix: str) -> list[dict[str, str]]:
    return [row for row in _all_rows() if row["ID"].startswith(prefix)]


def test_map_doc_exists_with_required_sections() -> None:
    text = _doc_text()
    for fragment in (
        "Crecimiento de operaciones vs crecimiento del kernel",
        "Compatibilidad con el catálogo 00–37",
        "Decisión deployment-by-agent",
        "Candidatos de cambio de kernel",
        "no otorga permiso",
        "Ninguna operación PM-written se elimina",
        "Aplicado en #376",
    ):
        assert fragment in text, f"map doc must contain: {fragment}"


def test_every_pm_written_operation_is_preserved_verbatim() -> None:
    for phase, wordings in PM_WRITTEN_OPERATIONS.items():
        rows = _section_rows(PHASE_ROW_PREFIXES[phase])
        assert len(rows) == len(wordings), (
            f"{phase}: expected {len(wordings)} rows, found {len(rows)}"
        )
        cells = [row["Enunciado PM original"] for row in rows]
        for wording in wordings:
            assert wording in cells, f"{phase}: PM wording dropped or altered: {wording}"


def test_every_accepted_recommended_operation_is_mapped() -> None:
    rows = _section_rows(RECOMMENDED_ROW_PREFIX)
    assert len(rows) == len(ACCEPTED_RECOMMENDED_OPERATIONS)
    cells = [row["Enunciado PM original"] for row in rows]
    for wording in ACCEPTED_RECOMMENDED_OPERATIONS:
        assert wording in cells, f"accepted recommended operation missing: {wording}"
    for row in rows:
        assert "accepted-recommended" in row["Clasificación"], (
            f"{row['ID']} must be classified accepted-recommended"
        )


def test_every_row_has_complete_contract_fields() -> None:
    for row in _all_rows():
        rid = row["ID"]
        assert row["Operación"], f"{rid}: missing short name"
        for token in ("Hace:", "Para:", "Cómo:"):
            assert token in row["Descripción"], f"{rid}: Descripción missing {token}"
        for token in ("Prev:", "Next:", "Rec:"):
            assert token in row["Conexiones"], f"{rid}: Conexiones missing {token}"
        assert "Req:" in row["Variables"] and "Opc:" in row["Variables"], (
            f"{rid}: Variables must declare Req/Opc"
        )
        assert row["Riesgo"] in RISK_TOKENS, f"{rid}: invalid risk {row['Riesgo']}"
        assert row["Exposición"] in EXPOSURE_TOKENS, f"{rid}: invalid exposure"
        assert row["Aprobación PM"], f"{rid}: missing PM approval behavior"
        assert CLASSIFICATION_TOKENS & set(re.findall(r"[a-z-]+", row["Clasificación"])), (
            f"{rid}: classification must use the shared vocabulary: {row['Clasificación']}"
        )
        assert "template:" in row["Kernel/Template"] and "kernel:" in row["Kernel/Template"], (
            f"{rid}: Kernel/Template must state template reuse and kernel impact"
        )
        for token in ("sec:", "env:", "notes:", "pre-release:"):
            assert token in row["Postura"], f"{rid}: Postura missing {token}"


def test_map_kernel_ids_resolve_and_deploy_candidates_are_applied() -> None:
    text = _doc_text()
    kernel_ids = _kernel_ids()
    referenced = set(KERNEL_ID_PATTERN.findall(text))
    unresolved = referenced - kernel_ids
    assert unresolved == set(), f"map references unknown kernel ids: {sorted(unresolved)}"
    # #376 applied the three deploy-execution candidates; they now resolve in the kernel.
    applied = KERNEL_CHANGE_CANDIDATE_IDS & kernel_ids
    assert applied == KERNEL_CHANGE_CANDIDATE_IDS, (
        f"deploy-execution kernel ids must be applied: missing {sorted(KERNEL_CHANGE_CANDIDATE_IDS - applied)}"
    )
    for candidate in KERNEL_CHANGE_CANDIDATE_IDS:
        assert candidate in text, f"applied id {candidate} must stay documented in the map"


def test_operation_growth_is_distinguished_from_kernel_growth() -> None:
    applied_rows = {row["ID"] for row in _all_rows() if "kernel:applied" in row["Kernel/Template"]}
    candidate_rows = {row["ID"] for row in _all_rows() if "kernel:candidate" in row["Kernel/Template"]}
    # #376 applied kernel ids only to local/staging deploy execution.
    assert applied_rows == {"MOS-5.11", "MOS-5.13"}, (
        f"only local/staging deploy rows apply kernel ids: {sorted(applied_rows)}"
    )
    # Production deploy execution stays the single remaining kernel candidate.
    assert candidate_rows == {"MOS-5.15"}, (
        f"only production deploy execution stays a kernel candidate: {sorted(candidate_rows)}"
    )
    for row in _all_rows():
        if row["ID"] not in DEPLOY_EXECUTE_ROW_IDS:
            assert "kernel:no-change" in row["Kernel/Template"], (
                f"{row['ID']}: operation growth must not imply kernel growth"
            )


def test_template_reuse_references_resolve() -> None:
    templates_dir = REPO_ROOT / "legacy-project-os" / "templates" / "operations"
    existing_indexes = {path.name[:2] for path in templates_dir.glob("*.md")}
    for row in _all_rows():
        for match in re.finditer(r"(?:reuse|exists)-(\d{2})", row["Kernel/Template"]):
            assert match.group(1) in existing_indexes, (
                f"{row['ID']}: references missing template {match.group(1)}"
            )


def test_deploy_by_agent_rows_are_internal_only_and_secret_safe() -> None:
    rows = _rows_by_id()
    for rid in DEPLOY_EXECUTE_ROW_IDS:
        row = rows[rid]
        assert row["Superficie"] == "terminal_agent", f"{rid}: must be terminal_agent"
        assert row["Exposición"] == "internal-only", f"{rid}: must be internal-only"
        assert "Sí (exacta" in row["Aprobación PM"], f"{rid}: needs exact PM approval"
        assert "sec:strict" in row["Postura"], f"{rid}: needs strict secret posture"
        assert "notes:req" in row["Postura"], f"{rid}: needs target Project-specific notes"
    for rid in INTERNAL_ONLY_ROW_IDS:
        row = rows[rid]
        assert row["Exposición"] == "internal-only", f"{rid}: must be internal-only"
        assert "pre-release:convert" in row["Postura"], (
            f"{rid}: internal-only rows must be removed/hidden/converted before public release"
        )
    for row in rows.values():
        if row["Exposición"] == "internal-only":
            assert "pre-release:convert" in row["Postura"], (
                f"{row['ID']}: internal-only requires a pre-release conversion posture"
            )


def test_deployment_decision_requirements_are_each_mapped() -> None:
    tables = _parse_tables(_doc_text(), "Requisito de despliegue del issue")
    rows = [row for section_rows in tables.values() for row in section_rows]
    assert len(rows) == len(DEPLOYMENT_DECISION_REQUIREMENTS)
    known_ids = set(_rows_by_id())
    mapped = {row["Requisito de despliegue del issue"]: row["Fila MOSDLC"] for row in rows}
    for requirement in DEPLOYMENT_DECISION_REQUIREMENTS:
        assert requirement in mapped, f"deployment requirement unmapped: {requirement}"
        for rid in re.findall(r"MOS-[R0-9]+\.\d+", mapped[requirement]):
            assert rid in known_ids, f"{requirement}: row {rid} does not exist"


def test_deployment_section_keeps_secret_safety_and_authority_constraints() -> None:
    text = _doc_text()
    for fragment in (
        "Project-specific notes",
        "aprobación PM exacta",
        "[REDACTED]",
        "printenv",
        "el despliegue queda con el Humano PM",
        "TARGET_ENVIRONMENT",
    ):
        assert fragment in text, f"deployment decision section must contain: {fragment}"


def test_legacy_catalog_00_37_is_fully_mapped() -> None:
    tables = _parse_tables(_doc_text(), "Op")
    rows = [row for section_rows in tables.values() for row in section_rows]
    ops = {row["Op"] for row in rows}
    expected = {f"{i:02d}" for i in range(38)}
    assert ops == expected, f"legacy catalog coverage drifted: missing {expected - ops}"
    known_ids = set(_rows_by_id())
    for row in rows:
        assert row["Estado MOSDLC"] in LEGACY_STATE_TOKENS, (
            f"op {row['Op']}: invalid legacy state {row['Estado MOSDLC']}"
        )
        target_ids = re.findall(r"MOS-[R0-9]+\.\d+", row["Filas MOSDLC destino"])
        assert target_ids, f"op {row['Op']}: must map to at least one MOSDLC row"
        for rid in target_ids:
            assert rid in known_ids, f"op {row['Op']}: unknown MOSDLC row {rid}"


def test_kernel_change_candidates_table_is_justified_and_resolved() -> None:
    text = _doc_text()
    tables = _parse_tables(text, "Candidato")
    rows = [row for section_rows in tables.values() for row in section_rows]
    named = {row["Candidato"].strip("`") for row in rows}
    assert named == KERNEL_CHANGE_CANDIDATE_IDS, (
        f"candidate table drifted from the declared candidates: {sorted(named)}"
    )
    for row in rows:
        assert row["Justificación"], f"{row['Candidato']}: candidate needs a justification"
        # #376 applied all three; the table must record the application, not defer it.
        assert "Aplicado en #376" in row["Decisión"], (
            f"{row['Candidato']}: decision must record the #376 application"
        )
    # Any further kernel id still requires a separate PM-approved issue.
    assert "aprobación PM exacta" in text


def test_connections_reference_existing_rows() -> None:
    known_ids = set(_rows_by_id())
    for row in _all_rows():
        for rid in re.findall(r"MOS-[R0-9]+\.\d+", row["Conexiones"]):
            assert rid in known_ids, f"{row['ID']}: connection to unknown row {rid}"
