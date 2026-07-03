"""Deterministic kernel resolver for project-os-v2-min.

Reads the current kernel JSON files at runtime and resolves actor, workflow,
and execution_mode selectors into expanded definitions with all referenced
evidence, output, and boundary entries.

This resolver is an optional deterministic accelerator for repo-local and
terminal use.  It reads kernel JSON at runtime and never duplicates kernel
data.  Resolver output shapes responses only and never grants permission
(boundary.output_not_permission).

Exit codes: 0 = resolved, 1 = resolution error, 2 = tooling error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_kernel(kernel_dir: Path) -> tuple[dict[str, Any], list[str]]:
    """Load manifest and all kernel files per load_order.

    Returns the loaded data keyed by family and any errors encountered.
    """
    errors: list[str] = []
    manifest_path = kernel_dir / "manifest.json"

    if not kernel_dir.is_dir():
        errors.append(f"kernel directory not found: {kernel_dir}")
        return {}, errors

    if not manifest_path.is_file():
        errors.append(f"manifest.json not found in {kernel_dir}")
        return {}, errors

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"manifest.json unreadable or invalid: {exc}")
        return {}, errors

    load_order = manifest.get("load_order", [])
    if not isinstance(load_order, list):
        errors.append("manifest load_order is not a list")
        return {}, errors

    data: dict[str, Any] = {"manifest": manifest}

    for filename in load_order:
        path = kernel_dir / filename
        if not path.is_file():
            errors.append(f"kernel file declared in load_order not found: {filename}")
            continue
        try:
            file_data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{filename} unreadable or invalid: {exc}")
            continue
        family = file_data.get("family")
        if not family:
            errors.append(f"{filename} missing 'family' field")
            continue
        data[family] = file_data

    return data, errors


def _build_index(data: dict[str, Any], family: str) -> dict[str, dict[str, Any]]:
    """Build an id-keyed index from a kernel family's entries list."""
    file_data = data.get(family, {})
    entries = file_data.get("entries", [])
    return {
        entry["id"]: entry
        for entry in entries
        if isinstance(entry, dict) and "id" in entry
    }


def _resolve_actor(
    actor_id: str,
    actors_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Look up and return the actor entry, or errors."""
    actor = actors_index.get(actor_id)
    if actor is None:
        known = sorted(actors_index.keys())
        return None, [f"actor '{actor_id}' not found in actors.json (known: {known})"]
    return dict(actor), []


def _resolve_workflow(
    workflow_id: str,
    workflows_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Look up and return the workflow entry, or errors."""
    workflow = workflows_index.get(workflow_id)
    if workflow is None:
        known = sorted(workflows_index.keys())
        return None, [f"workflow '{workflow_id}' not found in workflows.json (known: {known})"]
    return dict(workflow), []


def _resolve_mode(
    mode_id: str,
    modes_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Look up and return the execution_mode entry, or errors."""
    mode = modes_index.get(mode_id)
    if mode is None:
        known = sorted(modes_index.keys())
        return None, [f"execution_mode '{mode_id}' not found in execution_modes.json (known: {known})"]
    return dict(mode), []


WRITE_CAPABLE_ACTIONS = {
    "edit_scoped_files",
    "commit",
    "push_work_branch",
    "open_draft_pr",
    # Deployment execution mutates live target environments; it is write-capable
    # and, like repo-write modes, may only be paired with a terminal surface.
    "run_target_owned_deploy_commands",
}


def _check_compatibility(
    actor: dict[str, Any],
    workflow: dict[str, Any],
    mode: dict[str, Any],
) -> list[str]:
    """Validate that the workflow and mode are allowed for this actor."""
    errors: list[str] = []
    actor_id = actor.get("id", "unknown")
    workflow_id = workflow.get("id", "unknown")
    mode_id = mode.get("id", "unknown")

    # Actor allowed_mode_refs gates which modes this actor may use.
    allowed_modes = actor.get("allowed_mode_refs", [])
    if mode_id not in allowed_modes:
        errors.append(
            f"mode '{mode_id}' is not in actor '{actor_id}' allowed_mode_refs "
            f"(allowed: {allowed_modes})"
        )

    # Workflow compatibility: if a workflow requires branch preflight (local edits)
    # or PM approval (writes), it is a write-capable workflow and cannot be run
    # under a read-only mode.
    mode_actions = set(mode.get("allowed_actions", []))
    is_read_only_mode = not bool(mode_actions & WRITE_CAPABLE_ACTIONS)

    req_evidence = workflow.get("required_evidence_refs", [])
    is_write_workflow = (
        "evidence.branch_preflight" in req_evidence or
        "evidence.pm_approval" in req_evidence
    )

    if is_write_workflow and is_read_only_mode:
        errors.append(
            f"workflow '{workflow_id}' requires write capabilities "
            f"but mode '{mode_id}' is read-only"
        )

    return errors


def _expand_evidence(
    evidence_refs: list[str],
    evidence_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Expand evidence refs into full definitions. Return expanded dict and errors."""
    expanded: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for ref in evidence_refs:
        entry = evidence_index.get(ref)
        if entry is None:
            errors.append(f"evidence ref '{ref}' not found in evidence.json")
        else:
            expanded[ref] = dict(entry)
    return expanded, errors


def _expand_outputs(
    output_refs: list[str],
    outputs_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Expand output refs into full definitions. Return expanded dict and errors."""
    expanded: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for ref in output_refs:
        entry = outputs_index.get(ref)
        if entry is None:
            errors.append(f"output ref '{ref}' not found in outputs.json")
        else:
            expanded[ref] = dict(entry)
    return expanded, errors


def _expand_boundaries(
    boundary_refs: list[str],
    boundaries_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Expand boundary refs into full definitions. Return expanded dict and errors."""
    expanded: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for ref in boundary_refs:
        entry = boundaries_index.get(ref)
        if entry is None:
            errors.append(f"boundary ref '{ref}' not found in boundaries.json")
        else:
            expanded[ref] = dict(entry)
    return expanded, errors


def resolve(
    actor_id: str,
    workflow_id: str,
    mode_id: str,
    kernel_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Resolve actor + workflow + mode selectors against the live kernel.

    Returns a result dict with 'resolved', 'status', and 'errors' keys.
    """
    if kernel_dir is None:
        kernel_dir = Path(".") / "kernel"
    else:
        kernel_dir = Path(kernel_dir)

    # Load all kernel files following manifest load_order.
    data, load_errors = _load_kernel(kernel_dir)
    if load_errors:
        return {"resolved": None, "status": "error", "errors": load_errors}

    # Build indexes from kernel entries.
    actors_index = _build_index(data, "actors")
    workflows_index = _build_index(data, "workflows")
    modes_index = _build_index(data, "execution_modes")
    evidence_index = _build_index(data, "evidence")
    outputs_index = _build_index(data, "outputs")
    boundaries_index = _build_index(data, "boundaries")

    all_errors: list[str] = []

    # Resolve each selector.
    actor, errs = _resolve_actor(actor_id, actors_index)
    all_errors.extend(errs)

    workflow, errs = _resolve_workflow(workflow_id, workflows_index)
    all_errors.extend(errs)

    mode, errs = _resolve_mode(mode_id, modes_index)
    all_errors.extend(errs)

    # Fail closed on unresolvable selectors before compatibility check.
    if all_errors:
        return {"resolved": None, "status": "error", "errors": all_errors}

    # Validate compatibility.
    assert actor is not None and workflow is not None and mode is not None
    compat_errors = _check_compatibility(actor, workflow, mode)
    if compat_errors:
        return {"resolved": None, "status": "error", "errors": compat_errors}

    # Expand referenced definitions.

    # Evidence: union of workflow + mode required evidence refs.
    workflow_evidence_refs = workflow.get("required_evidence_refs", [])
    mode_evidence_refs = mode.get("required_evidence_refs", [])
    # Preserve order, deduplicate.
    seen_evidence: set[str] = set()
    effective_evidence_refs: list[str] = []
    for ref in workflow_evidence_refs + mode_evidence_refs:
        if ref not in seen_evidence:
            seen_evidence.add(ref)
            effective_evidence_refs.append(ref)

    evidence, errs = _expand_evidence(effective_evidence_refs, evidence_index)
    all_errors.extend(errs)

    # Outputs: from workflow allowed_output_refs.
    output_refs = workflow.get("allowed_output_refs", [])
    outputs, errs = _expand_outputs(output_refs, outputs_index)
    all_errors.extend(errs)

    # Boundaries: manifest states all boundaries always apply.
    # We include all global/hard boundaries plus any actor-specific ones.
    global_boundary_refs = sorted(boundaries_index.keys())
    actor_boundary_refs = actor.get("boundary_refs", [])
    effective_boundary_refs = sorted(set(global_boundary_refs) | set(actor_boundary_refs))

    boundaries, errs = _expand_boundaries(effective_boundary_refs, boundaries_index)
    all_errors.extend(errs)

    if all_errors:
        return {"resolved": None, "status": "error", "errors": all_errors}

    # Build the effective resolution summary.
    effective = _build_effective(
        actor, workflow, mode, effective_evidence_refs, evidence, effective_boundary_refs
    )

    resolved = {
        "actor": actor,
        "workflow": workflow,
        "execution_mode": mode,
        "evidence": evidence,
        "outputs": outputs,
        "boundaries": boundaries,
        "effective": effective,
    }

    return {
        "resolved": resolved,
        "status": "ok",
        "errors": [],
        "non_authorization": (
            "This resolution output shapes responses only. "
            "It never grants write permission, authorization, merge, "
            "closure, or any action authority. Permission comes only from "
            "exact scoped PM approval plus kernel-resolved gates."
        ),
    }


def _build_effective(
    actor: dict[str, Any],
    workflow: dict[str, Any],
    mode: dict[str, Any],
    effective_evidence_refs: list[str],
    evidence: dict[str, dict[str, Any]],
    effective_boundary_refs: list[str],
) -> dict[str, Any]:
    """Build the effective resolution summary combining actor, workflow, and mode."""
    # Effective allowed actions: mode's allowed_actions constrained by actor capabilities.
    mode_allowed = set(mode.get("allowed_actions", []))
    mode_prohibited = set(mode.get("prohibited_actions", []))

    # Actor denied actions are always denied regardless of mode.
    actor_denied = set(actor.get("denied_actions", []))

    # We explicitly model unresolved action mapping since exact normalization
    # isn't strictly enforced between actor capabilities and mode allowed actions.
    effective_allowed = sorted(mode_allowed - actor_denied)
    effective_prohibited = sorted(mode_prohibited | actor_denied)

    # Missing evidence: evidence entries whose missing_status is not status.resolved.
    missing_evidence: list[dict[str, str]] = []
    for ref in effective_evidence_refs:
        entry = evidence.get(ref, {})
        missing_status = entry.get("missing_status")
        if missing_status:
            missing_evidence.append({
                "evidence_id": ref,
                "missing_status": missing_status,
            })

    return {
        "effective_evidence_refs": effective_evidence_refs,
        "effective_allowed_actions": effective_allowed,
        "effective_prohibited_actions": effective_prohibited,
        "unresolved_actor_capabilities": sorted(set(actor.get("capabilities", []))),
        "actor_denied_actions": sorted(actor_denied),
        "effective_boundary_refs": effective_boundary_refs,
        "missing_evidence_statuses": missing_evidence,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the kernel resolver."""
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic kernel resolver for project-os-v2-min. "
            "Reads kernel JSON at runtime and resolves actor, workflow, "
            "and execution_mode selectors into expanded definitions."
        ),
    )
    parser.add_argument(
        "--actor",
        required=True,
        help="Actor selector, e.g. actor.terminal_agent",
    )
    parser.add_argument(
        "--workflow",
        required=True,
        help="Workflow selector, e.g. workflow.issue_implementation",
    )
    parser.add_argument(
        "--mode",
        required=True,
        help="Execution mode selector, e.g. mode.delegated_commit_pr",
    )
    parser.add_argument(
        "--kernel-dir",
        default=None,
        help="Path to kernel/ directory (default: ./kernel)",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Omit indentation from JSON output",
    )
    args = parser.parse_args(argv)

    try:
        result = resolve(
            actor_id=args.actor,
            workflow_id=args.workflow,
            mode_id=args.mode,
            kernel_dir=args.kernel_dir,
        )
    except Exception as exc:
        # Fail closed on unexpected tooling errors.
        error_result = {
            "resolved": None,
            "status": "error",
            "errors": [f"tooling error: {exc}"],
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        return 2

    indent = None if args.compact else 2
    print(json.dumps(result, indent=indent))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
