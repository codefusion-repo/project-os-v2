"""Read-only integrity validator for an allowed Project OS kernel.

Spanish remains the default; callers may explicitly validate the parallel
English kernel. Every other kernel path fails closed.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from tools.project_os_surfaces import DEFAULT_KERNEL_DIR, SURFACES, ProjectOSSurface, select_surface
except ModuleNotFoundError:  # Direct ``python tools/validate_kernel.py`` execution.
    from project_os_surfaces import DEFAULT_KERNEL_DIR, SURFACES, ProjectOSSurface, select_surface  # type: ignore[no-redef]

CANONICAL_STATUSES = {"status.resolved", "status.needs_context", "status.needs_pm_decision", "status.blocked"}
MATERIALITY_VALUES = ["material", "auxiliary"]
SOURCE_CATALOG = [
    "source.live_work_unit",
    "source.live_change_request",
    "source.live_target_record",
    "source.verified_adr",
    "source.verified_pm_decision",
    "source.local_branch_preflight",
    "source.live_repository_state",
    "source.verified_repository_adapter",
    "source.live_pm_decision",
    "source.agent_validation_output",
    "source.ci_validation_output",
    "source.live_change_diff",
    "source.exact_commit_range_diff",
    "source.live_review_record",
    "source.live_closure_record",
    "source.live_target_adoption",
    "source.verified_target_adapter",
    "source.live_deployment_readiness",
    "source.exact_target_ref",
    "source.live_auxiliary_context",
    "source.verified_auxiliary_context",
]
ACTION_CLASSES = {"action.read_only", "action.draft_only", "action.mutable"}
SAFE_DEGRADATION_KEY = "safe_degradation.non_material_gaps"
SAFE_GAP_FIELDS = [
    "verified_evidence",
    "unavailable_evidence",
    "materiality",
    "decision_impact",
    "equivalent_source_used",
    "revalidation_required_before_write",
]
MATERIALITY_CONTRACT = {
    "allowed_values": MATERIALITY_VALUES,
    "source_catalog": SOURCE_CATALOG,
    "minimum_evidence_field": "minimum_evidence",
    "safe_gap_materiality": "auxiliary",
    "hard_gates_degradable": False,
    "source_unavailability_signals": [
        "error.connector",
        "error.api",
        "error.network",
        "http.404",
        "http.422",
        "http.502",
    ],
    "source_error_target_state_inference": False,
    "truncation_material_impacts": [
        "impact.authority",
        "impact.scope",
        "impact.decision",
    ],
    "unclassified_truncation_fails_closed": True,
    "equivalent_source_requires": ["verifiable", "substitution_recorded"],
}
SAFE_DEGRADATION_CONTRACT = {
    "key": SAFE_DEGRADATION_KEY,
    "status_key": "status.resolved",
    "allowed_action_classes": ["action.read_only", "action.draft_only"],
    "requires_all_minimum_evidence": True,
    "gap_fields": SAFE_GAP_FIELDS,
    "completion_claim_with_gaps": False,
    "revalidation_required_before_write": True,
}
SHA_PATTERN = re.compile(r"\b[0-9a-f]{40}\b")
FORBIDDEN_KEYS = {"write_authorization_granted", "write_authorized", "permission_granted", "approval_granted"}


@dataclass(frozen=True)
class Finding:
    code: str
    file: str
    message: str

    def render(self) -> str:
        return f"{self.code} {self.file}: {self.message}"


def _load(
    kernel_dir: Path, surface: ProjectOSSurface, findings: list[Finding]
) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for family, (filename, collection) in surface.kernel_files.items():
        path = kernel_dir / filename
        if not path.is_file():
            findings.append(Finding("KES-001", filename, "required kernel file is missing"))
            continue
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("KES-001", filename, f"unreadable or invalid JSON: {exc}"))
            continue
        entries = content.get(collection) if isinstance(content, dict) else None
        if not isinstance(entries, list):
            findings.append(Finding("KES-002", filename, f"missing list '{collection}'"))
            continue
        data[family] = [entry for entry in entries if isinstance(entry, dict) and entry.get("active")]
        contract_field = {
            "evidence": "materiality_contract",
            "outputs": "safe_degradation_contract",
        }.get(family)
        if contract_field is not None:
            contract = content.get(contract_field)
            if not isinstance(contract, dict):
                findings.append(Finding("KES-012", filename, f"missing object '{contract_field}'"))
            else:
                data[contract_field] = contract
    return data


def _index(entries: list[dict[str, Any]], filename: str, findings: list[Finding]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for entry in entries:
        key = entry.get("key")
        if not isinstance(key, str):
            findings.append(Finding("KES-003", filename, "active entry is missing string key"))
        elif key in indexed:
            findings.append(Finding("KES-004", filename, f"duplicate active key '{key}'"))
        else:
            indexed[key] = entry
    return indexed


def _check_reference(index: dict[str, dict[str, Any]], key: Any, filename: str, findings: list[Finding]) -> None:
    if not isinstance(key, str) or key not in index:
        findings.append(Finding("KES-005", filename, f"unresolved active reference: {key!r}"))


def _check_project_markdown(path_value: Any, prefix: tuple[str, ...], filename: str, kernel_dir: Path, findings: list[Finding]) -> None:
    path = Path(path_value) if isinstance(path_value, str) else None
    if path is None or path.is_absolute() or path.parts[: len(prefix)] != prefix or path.suffix != ".md" or not (kernel_dir.parent.parent / path).is_file():
        findings.append(Finding("KES-006", filename, f"invalid or missing active Markdown path: {path_value!r}"))


def _check_durable_safety(kernel_dir: Path, findings: list[Finding]) -> None:
    for path in kernel_dir.glob("*.json"):
        text = path.read_text(encoding="utf-8")
        if "github.com/" in text or SHA_PATTERN.search(text):
            findings.append(Finding("KES-007", path.name, "live GitHub or commit state is forbidden in the kernel"))
        try:
            content = json.loads(text)
        except json.JSONDecodeError:
            continue
        stack: list[Any] = [content]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in FORBIDDEN_KEYS:
                        findings.append(Finding("KES-008", path.name, f"permission-grant field '{key}' is forbidden"))
                    stack.append(child)
            elif isinstance(value, list):
                stack.extend(value)


def _check_materiality_schema(
    data: dict[str, Any],
    surface: ProjectOSSurface,
    indexes: dict[str, dict[str, dict[str, Any]]],
    findings: list[Finding],
) -> None:
    evidence_file = surface.kernel_files["evidence"][0]
    workflow_file = surface.kernel_files["workflows"][0]
    output_file = surface.kernel_files["outputs"][0]
    materiality_contract = data.get("materiality_contract")
    safe_contract = data.get("safe_degradation_contract")
    if materiality_contract != MATERIALITY_CONTRACT:
        findings.append(
            Finding("KES-012", evidence_file, "materiality_contract does not match the canonical schema")
        )
    if safe_contract != SAFE_DEGRADATION_CONTRACT:
        findings.append(
            Finding("KES-015", output_file, "safe_degradation_contract does not match the canonical schema")
        )

    evidence = indexes["evidence"]
    for item in data["evidence"]:
        key = item.get("key")
        materiality = item.get("materiality")
        hard_gate = item.get("hard_gate")
        if materiality not in MATERIALITY_VALUES:
            findings.append(Finding("KES-013", evidence_file, f"{key!r} has unknown materiality {materiality!r}"))
        if not isinstance(hard_gate, bool):
            findings.append(Finding("KES-013", evidence_file, f"{key!r} is missing a boolean hard_gate"))
        elif hard_gate and materiality != "material":
            findings.append(Finding("KES-013", evidence_file, f"{key!r} hard gate must be material"))
        if item.get("revalidation_required_before_write") is not True:
            findings.append(
                Finding("KES-013", evidence_file, f"{key!r} must require revalidation before write")
            )
        source = item.get("source")
        if not isinstance(source, dict):
            findings.append(Finding("KES-013", evidence_file, f"{key!r} is missing its source contract"))
            continue
        primary = source.get("primary")
        equivalents = source.get("equivalents")
        if not isinstance(primary, str) or primary not in SOURCE_CATALOG:
            findings.append(Finding("KES-013", evidence_file, f"{key!r} has invalid primary source"))
        if not isinstance(equivalents, list):
            findings.append(Finding("KES-013", evidence_file, f"{key!r} equivalents must be a list"))
            continue
        seen_sources: set[str] = set()
        for equivalent in equivalents:
            source_key = equivalent.get("key") if isinstance(equivalent, dict) else None
            verification = equivalent.get("verification") if isinstance(equivalent, dict) else None
            if (
                not isinstance(source_key, str)
                or source_key not in SOURCE_CATALOG
                or source_key == primary
                or source_key in seen_sources
                or not isinstance(verification, str)
                or not verification.strip()
            ):
                findings.append(
                    Finding("KES-013", evidence_file, f"{key!r} has an invalid equivalent source")
                )
                continue
            seen_sources.add(source_key)

    for workflow in indexes["workflows"].values():
        key = workflow.get("key")
        required = workflow.get("required_evidence")
        minimum = workflow.get("minimum_evidence")
        if not isinstance(required, list) or not isinstance(minimum, list) or not minimum:
            findings.append(
                Finding("KES-014", workflow_file, f"{key!r} must declare non-empty evidence lists")
            )
            continue
        if len(required) != len(set(required)) or len(minimum) != len(set(minimum)):
            findings.append(Finding("KES-014", workflow_file, f"{key!r} has duplicate evidence"))
        if not set(minimum) <= set(required):
            findings.append(
                Finding("KES-014", workflow_file, f"{key!r} minimum_evidence is not a required-evidence subset")
            )
        for evidence_key in minimum:
            entry = evidence.get(evidence_key)
            if entry is not None and entry.get("materiality") != "material":
                findings.append(
                    Finding("KES-014", workflow_file, f"{key!r} minimum evidence {evidence_key!r} is not material")
                )
        for evidence_key in set(required) - set(minimum):
            entry = evidence.get(evidence_key)
            if entry is not None and entry.get("materiality") != "auxiliary":
                findings.append(
                    Finding("KES-014", workflow_file, f"{key!r} non-minimum evidence {evidence_key!r} is not auxiliary")
                )
        for evidence_key in required:
            entry = evidence.get(evidence_key)
            if entry is not None and key not in entry.get("workflow_key", []):
                findings.append(
                    Finding("KES-014", workflow_file, f"{evidence_key!r} does not declare workflow {key!r}")
                )

    for item in data["outputs"]:
        key = item.get("key")
        action_class = item.get("action_class")
        allows_gaps = item.get("allows_non_material_gaps")
        degradation_key = item.get("safe_degradation_key")
        if action_class not in ACTION_CLASSES:
            findings.append(Finding("KES-015", output_file, f"{key!r} has unknown action_class"))
        if not isinstance(allows_gaps, bool):
            findings.append(Finding("KES-015", output_file, f"{key!r} is missing gap policy"))
            continue
        if allows_gaps:
            if (
                action_class not in SAFE_DEGRADATION_CONTRACT["allowed_action_classes"]
                or item.get("status_key") != "status.resolved"
                or degradation_key != SAFE_DEGRADATION_KEY
            ):
                findings.append(Finding("KES-015", output_file, f"{key!r} has an unsafe gap policy"))
        elif degradation_key is not None:
            findings.append(
                Finding("KES-015", output_file, f"{key!r} references safe degradation while gaps are disabled")
            )


def _new_schema_projection(directory: Path, surface: ProjectOSSurface) -> dict[str, Any] | None:
    try:
        evidence_doc = json.loads((directory / surface.kernel_files["evidence"][0]).read_text(encoding="utf-8"))
        workflows_doc = json.loads((directory / surface.kernel_files["workflows"][0]).read_text(encoding="utf-8"))
        outputs_doc = json.loads((directory / surface.kernel_files["outputs"][0]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not all(isinstance(document, dict) for document in (evidence_doc, workflows_doc, outputs_doc)):
        return None

    def active_items(document: dict[str, Any], collection: str) -> list[dict[str, Any]]:
        entries = document.get(collection)
        if not isinstance(entries, list):
            return []
        return [item for item in entries if isinstance(item, dict) and item.get("active")]

    def evidence_projection(item: dict[str, Any]) -> dict[str, Any]:
        source = item.get("source")
        source = source if isinstance(source, dict) else {}
        equivalents = source.get("equivalents")
        equivalents = equivalents if isinstance(equivalents, list) else []
        return {
            "materiality": item.get("materiality"),
            "hard_gate": item.get("hard_gate"),
            "primary_source": source.get("primary"),
            "equivalent_sources": [
                equivalent.get("key")
                for equivalent in equivalents
                if isinstance(equivalent, dict)
            ],
            "revalidation_required_before_write": item.get("revalidation_required_before_write"),
        }

    return {
        "materiality_contract": evidence_doc.get("materiality_contract"),
        "safe_degradation_contract": outputs_doc.get("safe_degradation_contract"),
        "evidence": {
            item.get("key"): evidence_projection(item)
            for item in active_items(evidence_doc, "evidence")
        },
        "workflows": {
            item.get("key"): {
                "required_evidence": item.get("required_evidence"),
                "minimum_evidence": item.get("minimum_evidence"),
            }
            for item in active_items(workflows_doc, "workflows")
        },
        "outputs": {
            item.get("key"): {
                "status_key": item.get("status_key"),
                "action_class": item.get("action_class"),
                "allows_non_material_gaps": item.get("allows_non_material_gaps"),
                "safe_degradation_key": item.get("safe_degradation_key"),
            }
            for item in active_items(outputs_doc, "outputs")
        },
    }


def _check_bilingual_new_schema_parity(
    directory: Path, surface: ProjectOSSurface, findings: list[Finding]
) -> None:
    peer_surface = next(candidate for candidate in SURFACES if candidate.language != surface.language)
    peer_directory = directory.parent.parent / peer_surface.root_name / "kernel"
    if not peer_directory.is_dir():
        return
    current = _new_schema_projection(directory, surface)
    peer = _new_schema_projection(peer_directory, peer_surface)
    if current is not None and peer is not None and current != peer:
        findings.append(
            Finding("KES-016", str(directory), "evidence-materiality schema drift between ES and EN")
        )


def validate_kernel(kernel_dir: Path | str | None = None) -> list[Finding]:
    """Validate one exact allowed kernel directory and return all findings."""
    surface, directory = select_surface(kernel_dir)
    findings: list[Finding] = []
    if surface is None:
        surface = next(
            (
                candidate
                for candidate in SURFACES
                if directory.name == "kernel" and directory.parent.name == candidate.root_name
            ),
            None,
        )
    if surface is None:
        return [Finding("KES-011", str(directory), "kernel surface is not allowed")]
    data = _load(directory, surface, findings)
    if findings:
        return findings
    indexes = {
        family: _index(data[family], filename, findings)
        for family, (filename, _) in surface.kernel_files.items()
    }
    manifest = data["manifest"]
    if len(manifest) != 1:
        findings.append(Finding("KES-009", "manifest.json", "exactly one active manifest is required"))
        return findings
    manifest_key = manifest[0].get("key")
    rules = indexes["operational_rules"]
    if not any(rule.get("manifest_key") == manifest_key for rule in rules.values()):
        findings.append(
            Finding(
                "KES-005",
                surface.kernel_files["operational_rules"][0],
                "no active rule references the active manifest",
            )
        )

    actors, modes, workflows = indexes["actors"], indexes["modes"], indexes["workflows"]
    evidence, outputs, statuses = indexes["evidence"], indexes["outputs"], indexes["statuses"]
    for actor in actors.values():
        for mode in actor.get("allowed_modes", []):
            _check_reference(modes, mode, surface.kernel_files["actors"][0], findings)
    for workflow in workflows.values():
        for key in workflow.get("required_evidence", []):
            _check_reference(evidence, key, "workflows.json", findings)
        for key in workflow.get("minimum_evidence", []):
            _check_reference(evidence, key, "workflows.json", findings)
        for key in workflow.get("allowed_outputs", []):
            _check_reference(outputs, key, "workflows.json", findings)
    for limit in data["limits"]:
        if limit.get("actor_key") is not None:
            _check_reference(actors, limit.get("actor_key"), surface.kernel_files["limits"][0], findings)
        _check_reference(statuses, limit.get("on_violation"), surface.kernel_files["limits"][0], findings)
    for item in data["evidence"]:
        _check_reference(statuses, item.get("missing_status"), surface.kernel_files["evidence"][0], findings)
        for key in item.get("workflow_key", []):
            _check_reference(workflows, key, surface.kernel_files["evidence"][0], findings)
    for item in data["outputs"]:
        if item.get("status_key") is not None:
            _check_reference(statuses, item.get("status_key"), surface.kernel_files["outputs"][0], findings)
        for key in item.get("workflow_key", []):
            _check_reference(workflows, key, surface.kernel_files["outputs"][0], findings)
    for artifact in data["artifacts"]:
        for key in artifact.get("workflow_key", []):
            _check_reference(workflows, key, surface.kernel_files["artifacts"][0], findings)
        if artifact.get("output_key") is not None:
            _check_reference(outputs, artifact.get("output_key"), surface.kernel_files["artifacts"][0], findings)
        _check_project_markdown(
            artifact.get("required_template"),
            surface.templates_prefix,
            surface.kernel_files["artifacts"][0],
            directory,
            findings,
        )
    for skill in data["skills"]:
        _check_project_markdown(
            skill.get("required_skill"),
            surface.skills_prefix,
            surface.kernel_files["skills"][0],
            directory,
            findings,
        )
    if set(statuses) != CANONICAL_STATUSES:
        findings.append(Finding("KES-010", "estados.json", f"statuses must be exactly {sorted(CANONICAL_STATUSES)}"))
    _check_materiality_schema(data, surface, indexes, findings)
    _check_bilingual_new_schema_parity(directory, surface, findings)
    _check_durable_safety(directory, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel-dir", default=None, help="active kernel directory (default: ./project-os-es/kernel)")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args(argv)
    findings = validate_kernel(args.kernel_dir)
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    else:
        for finding in findings:
            print(finding.render())
        print(f"kernel validation: {'FAIL' if findings else 'OK'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
