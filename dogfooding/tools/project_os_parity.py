"""Structural parity diagnostics for the Spanish and English Project OS surfaces.

The report compares stable contracts, references, MOS codes, and variables. It
does not compare prose snapshots, line counts, or live project state.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from tools.operation_prompt_wizard import OperationTemplate, discover_operations
    from tools.project_os_surfaces import REPO_ROOT, SURFACES, ProjectOSSurface
except ModuleNotFoundError:  # Direct ``python dogfooding/tools/project_os_parity.py`` execution.
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tools.operation_prompt_wizard import OperationTemplate, discover_operations  # type: ignore[no-redef]
    from tools.project_os_surfaces import REPO_ROOT, SURFACES, ProjectOSSurface  # type: ignore[no-redef]


REFERENCE_FIELDS: dict[str, tuple[str, ...]] = {
    "operational_rules": ("manifest_key", "on_violation"),
    "actors": ("allowed_modes",),
    "modes": ("fallback",),
    "workflows": ("required_evidence", "minimum_evidence", "allowed_outputs"),
    "limits": ("actor_key", "on_violation"),
    "evidence": ("workflow_key", "missing_status"),
    "outputs": ("workflow_key", "status_key"),
    "artifacts": ("workflow_key", "output_key"),
}

STABLE_FIELDS: dict[str, tuple[str, ...]] = {
    "manifest": ("key", "version", "active"),
    "operational_rules": ("key", "manifest_key", "on_violation", "priority", "active"),
    "actors": ("key", "surface", "allowed_modes", "active"),
    "modes": ("key", "fallback", "active"),
    "workflows": ("key", "required_evidence", "minimum_evidence", "allowed_outputs", "active"),
    "limits": ("key", "actor_key", "on_violation", "blocking", "active"),
    "evidence": (
        "key",
        "workflow_key",
        "missing_status",
        "required",
        "materiality",
        "hard_gate",
        "revalidation_required_before_write",
        "active",
    ),
    "outputs": (
        "key",
        "workflow_key",
        "status_key",
        "action_class",
        "allows_non_material_gaps",
        "safe_degradation_key",
        "context_receipt_key",
        "active",
    ),
    "artifacts": ("key", "workflow_key", "output_key", "active"),
    "skills": ("key", "active"),
    "statuses": ("key", "type", "active"),
}

STRUCTURAL_LIST_FIELDS: dict[str, tuple[str, ...]] = {
    "manifest": ("resolution_sequence",),
    "operational_rules": ("resolution_sequence",),
    "workflows": ("required_behavior",),
    "outputs": ("must_include", "must_include_by_density"),
    "skills": ("use_for",),
}

ACTION_EQUIVALENCE = {
    "leer": "read",
    "analizar": "analyze",
    "ejecutar comandos read-only": "run read-only commands",
    "reportar": "report",
    "editar archivos scoped": "edit scoped files",
    "editar archivos": "edit files",
    "ejecutar validacion": "run validation",
    "commit": "commit",
    "push": "push",
    "push a la rama de trabajo": "push to the work branch",
    "abrir PR": "open a PR",
    "abrir draft PR": "open a draft PR",
    "comentar": "comment",
    "comentar fuera de scope": "comment outside scope",
    "merge": "merge",
    "cerrar la unidad de trabajo": "close the work unit",
    "aplicar labels": "apply labels",
    "crear tags o releases": "create tags or releases",
    "cambiar settings": "change settings",
    "ejecutar comandos de deploy target-owned para un unico entorno aprobado local o staging": "run target-owned deployment commands for one approved local or staging environment",
    "inventar comandos de deploy": "invent deployment commands",
    "deploy a produccion": "deploy to production",
    "exponer secretos": "expose secrets",
    "dumps amplios de entorno o configuracion": "run broad environment or configuration dumps",
    "mutar secret stores": "mutate secret stores",
    "mutar el target remoto": "mutate the remote target",
    "otra mutacion del target remoto": "perform another remote-target mutation",
}

PHASE_EQUIVALENCE = {
    "cross-fase": "cross-phase",
    "fase-0": "phase-0",
    "fase-1": "phase-1",
    "fase-2": "phase-2",
    "fase-3": "phase-3",
    "fase-4": "phase-4",
    "fase-5": "phase-5",
    "fase-6": "phase-6",
}

ENGLISH_PHASE_LABELS = {
    "cross-phase": "Cross-phase",
    "phase-0": "Phase 0 — Adoption",
    "phase-1": "Phase 1 — Requirements, planning, and feasibility",
    "phase-2": "Phase 2 — Design",
    "phase-3": "Phase 3 — Implementation",
    "phase-4": "Phase 4 — QA and human verification",
    "phase-5": "Phase 5 — Local, staging, and production deployment",
    "phase-6": "Phase 6 — Maintenance and improvements",
}

SURFACE_EQUIVALENCE = {
    "browser_chat a human_pm": "browser_chat → human_pm",
}

# Machine-consumed structure only: UPPER_SNAKE variable fields agents fill or
# grep, fenced-block layout, and shell command lines the PM copies and runs.
MACHINE_FIELD_PATTERN = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=", re.MULTILINE)
FENCED_BLOCK_PATTERN = re.compile(r"^```([A-Za-z/+-]*)\s*$", re.MULTILINE)
SHELL_COMMAND_PATTERN = re.compile(r"^\s*(?:gh|git|python3?|set|cat)\b.*$", re.MULTILINE)

# Route prompts are filled by the wizard/browser chat and grepped by the
# receiving agent; these variable names are executable contract, not prose.
ROUTE_PROMPT_REQUIRED_FIELDS = frozenset(
    {
        "PROJECT_NAME",
        "REPOSITORY_NAME",
        "TARGET_REPOSITORY",
        "KERNEL_REPOSITORY",
        "KERNEL_LOCAL_PATH",
        "WORK_UNIT",
        "CHANGE_CLASS",
        "TARGET_ACTOR_TYPE",
        "WORKFLOW",
        "EXECUTION_MODE",
        "OUTPUT_CONTRACT",
        "OPTIONAL_SKILL",
        "HYDRATION_LEVEL",
        "RECOMMENDED_TERMINAL_AGENT_FAMILY",
        "SCOPE",
        "OUT_OF_SCOPE",
        "EVIDENCE_REQUIRED",
        "VALIDATION_REQUIRED",
        "BRANCH_NAME",
        "PM_AUTHORIZATION_STATUS",
    }
)

TEMPLATE_PAIRS = {
    "README.md": "README.md",
    "adr.md": "adr.md",
    "comentario-cierre.md": "closure-comment.md",
    "issue.md": "issue.md",
    "paquete-adopcion.md": "adoption-packet.md",
    "paquete-handoff.md": "handoff-packet.md",
    "plan-implementacion-manual.md": "manual-implementation-plan.md",
    "pm-command-bundle.md": "pm-command-bundle.md",
    "prompt-asset.md": "asset-prompt.md",
    "prompt-revision-seguridad.md": "security-review-prompt.md",
    "pull-request.md": "pull-request.md",
    "reporte-ejecucion.md": "execution-report.md",
    "resultado-estado.md": "status-result.md",
    "resultado-revision.md": "review-result.md",
    "roadmap.md": "roadmap.md",
    "route-prompt.md": "route-prompt.md",
}

OPERATION_ID_PATTERN = re.compile(r"(?:Operación MOSDLC|MOSDLC operation) `([^`]+)`")
RISK_PATTERN = re.compile(r"(?:Riesgo|Risk):\s*([a-z]+)", re.IGNORECASE)
MOS_REF_PATTERN = re.compile(r"\bMOS-(?:\d+\.\d+|R\.\d+)\b", re.IGNORECASE)


@dataclass(frozen=True)
class OperationContract:
    code: str
    relative_path: str
    operation_id: str
    phase: str
    risk: str
    surface: str
    kernel: tuple[str, ...]
    evidence: tuple[str, ...]
    approval: str
    variables: tuple[tuple[str, bool], ...]
    outputs: tuple[str, ...]
    connections: tuple[str, ...]


def load_kernel(surface: ProjectOSSurface) -> dict[str, list[dict[str, Any]]]:
    loaded: dict[str, list[dict[str, Any]]] = {}
    for family, (filename, collection) in surface.kernel_files.items():
        content = json.loads((surface.kernel_dir / filename).read_text(encoding="utf-8"))
        loaded[family] = [
            item for item in content[collection] if isinstance(item, dict) and item.get("active")
        ]
    return loaded


def keyed(kernel: dict[str, list[dict[str, Any]]], family: str) -> dict[str, dict[str, Any]]:
    return {item["key"]: item for item in kernel[family]}


def stable_projection(kernel: dict[str, list[dict[str, Any]]], family: str) -> dict[str, dict[str, Any]]:
    return {
        key: {field: entry.get(field) for field in STABLE_FIELDS[family] if field != "key"}
        for key, entry in keyed(kernel, family).items()
    }


def reference_graph(kernel: dict[str, list[dict[str, Any]]]) -> set[tuple[str, str, str]]:
    graph: set[tuple[str, str, str]] = set()
    for family, fields in REFERENCE_FIELDS.items():
        for item in kernel[family]:
            for field in fields:
                value = item.get(field)
                references = value if isinstance(value, list) else [value]
                for reference in references:
                    if isinstance(reference, str):
                        graph.add((item["key"], field, reference))
    return graph


def _line(text: str, es_label: str, en_label: str) -> str:
    match = re.search(rf"^- (?:{re.escape(es_label)}|{re.escape(en_label)}):\s*(.+)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing operation metadata: {es_label}/{en_label}")
    return match.group(1).strip()


def _approval_category(value: str) -> str:
    lowered = value.lower()
    if lowered.startswith(("sí", "yes")):
        return "required"
    if lowered.startswith("no para draftear") or lowered.startswith("no for drafting"):
        return "draft_then_exact"
    return "not_required_for_this_operation"


def operation_contract(operation: OperationTemplate) -> OperationContract:
    text = operation.text
    operation_id = OPERATION_ID_PATTERN.search(text)
    risk = RISK_PATTERN.search(text)
    if not operation.mos_code or not operation_id or not risk:
        raise ValueError(f"incomplete operation metadata: {operation.path}")
    evidence = tuple(re.findall(r"evidence\.[a-z_]+", _line(text, "Evidencia", "Evidence")))
    outputs = tuple(sorted(set(re.findall(r"output\.[a-z_]+", text))))
    connections = tuple(sorted(set(match.upper() for match in MOS_REF_PATTERN.findall(text.split("**Connections:**", 1)[-1].split("**Conexiones:**", 1)[-1]))))
    return OperationContract(
        code=operation.mos_code,
        relative_path=operation.relative_path,
        operation_id=operation_id.group(1),
        phase=operation.phase_path,
        risk=risk.group(1).lower(),
        surface=_line(text, "Superficie", "Surface"),
        kernel=tuple(
            re.findall(
                r"(?:workflow|mode|output)\.[a-z_]+",
                _line(text, "Kernel", "Kernel"),
            )
        ),
        evidence=evidence,
        approval=_approval_category(_line(text, "Aprobación PM", "PM approval")),
        variables=tuple((variable.name, variable.required) for variable in operation.variables),
        outputs=outputs,
        connections=connections,
    )


def operation_inventory(root: Path) -> dict[str, OperationContract]:
    return {item.mos_code: operation_contract(item) for item in discover_operations(root)}


def _mapped_contract(contract: OperationContract) -> dict[str, Any]:
    return {
        "operation_id": contract.operation_id,
        "phase": PHASE_EQUIVALENCE.get(contract.phase, contract.phase),
        "risk": contract.risk,
        "surface": SURFACE_EQUIVALENCE.get(contract.surface, contract.surface),
        "kernel": contract.kernel,
        "evidence": contract.evidence,
        "approval": contract.approval,
        "variables": contract.variables,
        "outputs": contract.outputs,
        "connections": contract.connections,
    }


def _machine_fields(text: str) -> set[str]:
    return set(MACHINE_FIELD_PATTERN.findall(text))


def _fence_signature(text: str) -> tuple[str, ...]:
    """Opening fence languages in order; even entries open blocks, odd close."""

    return tuple(FENCED_BLOCK_PATTERN.findall(text)[::2])


def _shell_commands(text: str) -> tuple[str, ...]:
    """Command lines the PM copies verbatim; localized prose never matches."""

    return tuple(match.strip() for match in SHELL_COMMAND_PATTERN.findall(text))


def _operation_structural_findings(
    es_operations: dict[str, OperationTemplate],
    en_operations: dict[str, OperationTemplate],
) -> list[str]:
    """Check only operation structure with an executable consumer (the wizard)."""

    findings: list[str] = []
    description_markers = {"es": "**Hace:**", "en": "**Does:**"}
    for code in sorted(set(es_operations) & set(en_operations)):
        for language, operation in (("es", es_operations[code]), ("en", en_operations[code])):
            if description_markers[language] not in operation.text:
                findings.append(f"operation description marker missing: {language}:{code}")
    return findings


def _template_structural_findings(es_root: Path, en_root: Path) -> list[str]:
    """Compare template pairing, machine fields, fences, and copied commands."""

    findings: list[str] = []
    if set(path.name for path in es_root.glob("*.md")) != set(TEMPLATE_PAIRS):
        findings.append("Spanish template mapping is incomplete")
    if set(path.name for path in en_root.glob("*.md")) != set(TEMPLATE_PAIRS.values()):
        findings.append("English template mapping is incomplete")

    for es_name, en_name in TEMPLATE_PAIRS.items():
        es_path, en_path = es_root / es_name, en_root / en_name
        if not es_path.is_file() or not en_path.is_file():
            continue
        es_text = es_path.read_text(encoding="utf-8")
        en_text = en_path.read_text(encoding="utf-8")
        if _machine_fields(es_text) != _machine_fields(en_text):
            findings.append(f"template machine-field mismatch: {es_name}/{en_name}")
        if _fence_signature(es_text) != _fence_signature(en_text):
            findings.append(f"template fenced-block mismatch: {es_name}/{en_name}")
        if _shell_commands(es_text) != _shell_commands(en_text):
            findings.append(f"template shell-command mismatch: {es_name}/{en_name}")

    for root, name in ((es_root, "route-prompt.md"), (en_root, "route-prompt.md")):
        path = root / name
        if not path.is_file():
            continue
        missing = ROUTE_PROMPT_REQUIRED_FIELDS - _machine_fields(path.read_text(encoding="utf-8"))
        for field in sorted(missing):
            findings.append(f"route prompt field missing: {field}")

    for root in (es_root, en_root):
        path = root / "pm-command-bundle.md"
        if not path.is_file():
            continue
        if "--squash" in path.read_text(encoding="utf-8"):
            findings.append(f"PM command bundle uses a non-canonical squash merge: {root.name}")
    return findings


def _path_findings(surface: ProjectOSSurface, kernel: dict[str, list[dict[str, Any]]]) -> list[str]:
    findings: list[str] = []
    for artifact in kernel["artifacts"]:
        path = Path(artifact.get("required_template", ""))
        if path.parts[:2] != surface.templates_prefix or not (REPO_ROOT / path).is_file():
            findings.append(f"{surface.language}: invalid artifact template path for {artifact['key']}: {path}")
    for skill in kernel["skills"]:
        path = Path(skill.get("required_skill", ""))
        if path.parts[:2] != surface.skills_prefix or not (REPO_ROOT / path).is_file():
            findings.append(f"{surface.language}: invalid skill path for {skill['key']}: {path}")
    return findings


def build_report() -> dict[str, Any]:
    es_surface, en_surface = SURFACES
    es_kernel, en_kernel = load_kernel(es_surface), load_kernel(en_surface)
    structural_findings: list[str] = []

    for family in STABLE_FIELDS:
        es_projection = stable_projection(es_kernel, family)
        en_projection = stable_projection(en_kernel, family)
        if es_projection != en_projection:
            structural_findings.append(f"kernel stable-contract mismatch: {family}")

    def _list_shape(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: _list_shape(item) for key, item in sorted(value.items())}
        if isinstance(value, list):
            return len(value)
        return 0

    for family, fields in STRUCTURAL_LIST_FIELDS.items():
        es_items, en_items = keyed(es_kernel, family), keyed(en_kernel, family)
        for key in sorted(es_items):
            for field in fields:
                if _list_shape(es_items[key].get(field, [])) != _list_shape(en_items[key].get(field, [])):
                    structural_findings.append(f"kernel structural-list mismatch: {key}.{field}")

    if reference_graph(es_kernel) != reference_graph(en_kernel):
        structural_findings.append("kernel reference graph mismatch")

    for key, es_mode in keyed(es_kernel, "modes").items():
        en_mode = keyed(en_kernel, "modes")[key]
        for field in ("allowed_actions", "prohibited_actions"):
            translated = [ACTION_EQUIVALENCE[action] for action in es_mode[field]]
            if translated != en_mode[field]:
                structural_findings.append(f"mode action mismatch: {key}.{field}")

    structural_findings.extend(_path_findings(es_surface, es_kernel))
    structural_findings.extend(_path_findings(en_surface, en_kernel))

    es_templates = {
        item.mos_code: item for item in discover_operations(es_surface.root / "operaciones")
    }
    en_templates = {
        item.mos_code: item for item in discover_operations(en_surface.root / "operations")
    }
    es_operations = {code: operation_contract(item) for code, item in es_templates.items()}
    en_operations = {code: operation_contract(item) for code, item in en_templates.items()}
    if set(es_operations) != set(en_operations):
        structural_findings.append("MOS code set mismatch")
    for code in sorted(set(es_operations) & set(en_operations)):
        if _mapped_contract(es_operations[code]) != _mapped_contract(en_operations[code]):
            structural_findings.append(f"operation contract mismatch: {code}")

    structural_findings.extend(_operation_structural_findings(es_templates, en_templates))
    structural_findings.extend(
        _template_structural_findings(
            es_surface.root / "templates",
            en_surface.root / "templates",
        )
    )
    findings = list(structural_findings)

    return {
        "surfaces": {
            "default": es_surface.root_name,
            "explicit_english": en_surface.root_name,
        },
        "kernel_ids": {
            family: len(keyed(es_kernel, family)) for family in STABLE_FIELDS
        },
        "reference_edges": len(reference_graph(es_kernel)),
        "operations": {
            "mos_codes": len(es_operations),
            "variables": sorted({name for contract in es_operations.values() for name, _ in contract.variables}),
            "path_matrix": [
                {
                    "code": code,
                    "es": es_operations[code].relative_path,
                    "en": en_operations[code].relative_path,
                }
                for code in sorted(es_operations)
            ],
        },
        "structural_findings": structural_findings,
        "manual_review_required": [
            "natural PM-facing English across all operation and template pairs",
            "semantic fidelity beyond the automated structural contracts",
        ],
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit the full JSON report")
    args = parser.parse_args(argv)
    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"kernel ids: {sum(report['kernel_ids'].values())}")
        print(f"reference edges: {report['reference_edges']}")
        print(f"MOS codes: {report['operations']['mos_codes']}")
        print(f"variables: {len(report['operations']['variables'])}")
        print(f"structural findings: {len(report['structural_findings'])}")
        print("manual review: required for linguistic naturalness and semantic fidelity")
        print(f"parity findings: {len(report['findings'])}")
        for finding in report["findings"]:
            print(f"- {finding}")
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
