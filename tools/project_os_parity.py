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
except ModuleNotFoundError:  # Direct ``python tools/project_os_parity.py`` execution.
    from operation_prompt_wizard import OperationTemplate, discover_operations  # type: ignore[no-redef]
    from project_os_surfaces import REPO_ROOT, SURFACES, ProjectOSSurface  # type: ignore[no-redef]


REFERENCE_FIELDS: dict[str, tuple[str, ...]] = {
    "operational_rules": ("manifest_key", "on_violation"),
    "actors": ("allowed_modes",),
    "modes": ("fallback",),
    "workflows": ("required_evidence", "allowed_outputs"),
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
    "workflows": ("key", "required_evidence", "allowed_outputs", "active"),
    "limits": ("key", "actor_key", "on_violation", "blocking", "active"),
    "evidence": ("key", "workflow_key", "missing_status", "required", "active"),
    "outputs": ("key", "workflow_key", "status_key", "active"),
    "artifacts": ("key", "workflow_key", "output_key", "active"),
    "skills": ("key", "active"),
    "statuses": ("key", "type", "active"),
}

STRUCTURAL_LIST_FIELDS: dict[str, tuple[str, ...]] = {
    "manifest": ("resolution_sequence",),
    "operational_rules": ("resolution_sequence",),
    "workflows": ("required_behavior",),
    "outputs": ("must_include",),
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
        "surface": contract.surface,
        "kernel": contract.kernel,
        "evidence": contract.evidence,
        "approval": contract.approval,
        "variables": contract.variables,
        "outputs": contract.outputs,
        "connections": contract.connections,
    }


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
    findings: list[str] = []

    for family in STABLE_FIELDS:
        es_projection = stable_projection(es_kernel, family)
        en_projection = stable_projection(en_kernel, family)
        if es_projection != en_projection:
            findings.append(f"kernel stable-contract mismatch: {family}")

    for family, fields in STRUCTURAL_LIST_FIELDS.items():
        es_items, en_items = keyed(es_kernel, family), keyed(en_kernel, family)
        for key in sorted(es_items):
            for field in fields:
                if len(es_items[key].get(field, [])) != len(en_items[key].get(field, [])):
                    findings.append(f"kernel structural-list mismatch: {key}.{field}")

    if reference_graph(es_kernel) != reference_graph(en_kernel):
        findings.append("kernel reference graph mismatch")

    for key, es_mode in keyed(es_kernel, "modes").items():
        en_mode = keyed(en_kernel, "modes")[key]
        for field in ("allowed_actions", "prohibited_actions"):
            translated = [ACTION_EQUIVALENCE[action] for action in es_mode[field]]
            if translated != en_mode[field]:
                findings.append(f"mode action mismatch: {key}.{field}")

    findings.extend(_path_findings(es_surface, es_kernel))
    findings.extend(_path_findings(en_surface, en_kernel))

    es_operations = operation_inventory(es_surface.root / "operaciones")
    en_operations = operation_inventory(en_surface.root / "operations")
    if set(es_operations) != set(en_operations):
        findings.append("MOS code set mismatch")
    for code in sorted(set(es_operations) & set(en_operations)):
        if _mapped_contract(es_operations[code]) != _mapped_contract(en_operations[code]):
            findings.append(f"operation contract mismatch: {code}")

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
        print(f"parity findings: {len(report['findings'])}")
        for finding in report["findings"]:
            print(f"- {finding}")
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
