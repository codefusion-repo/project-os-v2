"""Single read-only integrity validator for the project-os-v2-min kernel.

The English kernel is archived under legacy-project-os/ (the active surface is
project-os-es/); this validator keeps the archived kernel internally coherent.

Checks the kernel/*.json files for:
- parseability and required envelope fields;
- manifest load_order parity with the files actually present;
- unique ids and resolvable internal references;
- exactly the four canonical resolution statuses;
- absence of permission-grant fields;
- absence of live state (SHAs, GitHub URLs, issue/PR state fields);
- actor surface safety (non-terminal surfaces never get write-capable modes);
- the kernel size budget declared in the manifest.

Exit codes: 0 = kernel valid, 1 = findings, 2 = tooling error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

CANONICAL_STATUSES = {
    "status.resolved",
    "status.needs_context",
    "status.needs_pm_decision",
    "status.blocked",
}

REF_PREFIXES = ("status.", "actor.", "mode.", "boundary.", "evidence.", "workflow.", "output.")
REF_PATTERN = re.compile(r"^(status|actor|mode|boundary|evidence|workflow|output)\.[a-z0-9_]+$")

PERMISSION_GRANT_KEYS = {
    "write_authorization_granted",
    "write_authorized",
    "can_write",
    "can_push",
    "can_merge",
    "can_close_issue",
    "approval_granted",
    "permission_granted",
}

LIVE_STATE_KEYS = {
    "issue_number",
    "pr_number",
    "branch_state",
    "merged_at",
    "closed_at",
    "validation_result",
    "head_sha",
    "commit_sha",
    "release_readiness",
}

SHA_PATTERN = re.compile(r"\b[0-9a-f]{40}\b")
GITHUB_URL_PATTERN = re.compile(r"github\.com/")

WRITE_CAPABLE_ACTIONS = {
    "edit_scoped_files",
    "commit",
    "push_work_branch",
    "open_draft_pr",
    # Deployment execution mutates live target environments; treat it as
    # write-capable so non-terminal actors can never be given a deploy mode.
    "run_target_owned_deploy_commands",
}

REQUIRED_ENTRY_KEYS = {
    "actors": {"id", "surface", "boundary_refs"},
    "execution_modes": {"id", "allowed_actions", "prohibited_actions"},
    "boundaries": {"id", "rule", "on_violation"},
    "evidence": {"id", "satisfied_by", "missing_status"},
    "workflows": {"id", "use_for", "required_evidence_refs", "allowed_output_refs"},
    "outputs": {"id", "use_for", "required_sections"},
    "statuses": {"id", "meaning"},
}


@dataclass
class Finding:
    code: str
    file: str
    pointer: str
    message: str
    severity: str = "error"

    def render(self) -> str:
        return f"{self.code} [{self.severity}] {self.file} {self.pointer}: {self.message}"


@dataclass
class Kernel:
    root: Path
    files: dict[str, dict[str, Any]] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)


def _walk(value: Any, pointer: str = "") -> Iterator[tuple[str, Any]]:
    yield pointer, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{pointer}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{pointer}/{index}")


def _load(kernel: Kernel) -> None:
    kernel_dir = kernel.root / "kernel"
    if not kernel_dir.is_dir():
        kernel.findings.append(Finding("KMIN-001", "kernel/", "", "kernel directory not found"))
        return
    for path in sorted(kernel_dir.glob("*.json")):
        rel = f"kernel/{path.name}"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            kernel.findings.append(Finding("KMIN-001", rel, "", f"unreadable or invalid JSON: {exc}"))
            continue
        if not isinstance(data, dict):
            kernel.findings.append(Finding("KMIN-001", rel, "", "top-level JSON value must be an object"))
            continue
        kernel.files[path.name] = data


def _check_manifest(kernel: Kernel) -> None:
    manifest = kernel.files.get("manifest.json")
    if manifest is None:
        kernel.findings.append(Finding("KMIN-001", "kernel/manifest.json", "", "manifest.json missing"))
        return
    for key in ("kernel_version", "load_order", "size_budget", "non_authorization"):
        if key not in manifest:
            kernel.findings.append(
                Finding("KMIN-003", "kernel/manifest.json", f"/{key}", f"manifest missing required field '{key}'")
            )
    declared = set(manifest.get("load_order", []))
    present = set(kernel.files) - {"manifest.json"}
    for name in sorted(declared - present):
        kernel.findings.append(
            Finding("KMIN-002", "kernel/manifest.json", "/load_order", f"declared file missing from kernel/: {name}")
        )
    for name in sorted(present - declared):
        kernel.findings.append(
            Finding("KMIN-002", f"kernel/{name}", "", "kernel file not declared in manifest load_order")
        )


def _check_envelopes_and_ids(kernel: Kernel) -> dict[str, str]:
    ids: dict[str, str] = {}
    for name, data in kernel.files.items():
        rel = f"kernel/{name}"
        for key in ("id", "family"):
            if key not in data:
                kernel.findings.append(Finding("KMIN-003", rel, f"/{key}", f"missing envelope field '{key}'"))
        family = data.get("family", "")
        required = REQUIRED_ENTRY_KEYS.get(family, set())
        for index, entry in enumerate(data.get("entries", [])):
            pointer = f"/entries/{index}"
            if not isinstance(entry, dict):
                kernel.findings.append(Finding("KMIN-003", rel, pointer, "entry must be an object"))
                continue
            entry_id = entry.get("id")
            if not isinstance(entry_id, str):
                kernel.findings.append(Finding("KMIN-003", rel, pointer, "entry missing string 'id'"))
            elif entry_id in ids:
                kernel.findings.append(
                    Finding("KMIN-004", rel, f"{pointer}/id", f"duplicate id '{entry_id}' (also in {ids[entry_id]})")
                )
            else:
                ids[entry_id] = rel
            missing = required - set(entry)
            for key in sorted(missing):
                kernel.findings.append(
                    Finding("KMIN-003", rel, pointer, f"{family} entry missing required key '{key}'")
                )
    return ids


def _check_references(kernel: Kernel, ids: dict[str, str]) -> None:
    for name, data in kernel.files.items():
        rel = f"kernel/{name}"
        for pointer, value in _walk(data):
            if not isinstance(value, str) or not value.startswith(REF_PREFIXES):
                continue
            if value.endswith(".json") or not REF_PATTERN.match(value):
                continue
            if pointer.endswith("/id"):
                continue
            if value.startswith("status.") and value not in CANONICAL_STATUSES:
                kernel.findings.append(
                    Finding("KMIN-006", rel, pointer, f"non-canonical status reference '{value}'")
                )
                continue
            if value not in ids:
                kernel.findings.append(Finding("KMIN-005", rel, pointer, f"unresolved reference '{value}'"))


def _check_statuses(kernel: Kernel) -> None:
    statuses = kernel.files.get("statuses.json")
    if statuses is None:
        return
    defined = {entry.get("id") for entry in statuses.get("entries", []) if isinstance(entry, dict)}
    if defined != CANONICAL_STATUSES:
        kernel.findings.append(
            Finding(
                "KMIN-007",
                "kernel/statuses.json",
                "/entries",
                f"statuses must be exactly {sorted(CANONICAL_STATUSES)}, found {sorted(d for d in defined if d)}",
            )
        )


def _check_forbidden_content(kernel: Kernel) -> None:
    for name, data in kernel.files.items():
        rel = f"kernel/{name}"
        for pointer, value in _walk(data):
            if isinstance(value, dict):
                for key in value:
                    if key in PERMISSION_GRANT_KEYS:
                        kernel.findings.append(
                            Finding("KMIN-008", rel, f"{pointer}/{key}", f"permission-grant field '{key}' is forbidden")
                        )
                    if key in LIVE_STATE_KEYS:
                        kernel.findings.append(
                            Finding("KMIN-009", rel, f"{pointer}/{key}", f"live-state field '{key}' is forbidden")
                        )
            elif isinstance(value, str):
                if SHA_PATTERN.search(value):
                    kernel.findings.append(
                        Finding("KMIN-009", rel, pointer, "40-hex SHA found; live git state is forbidden in the kernel")
                    )
                if GITHUB_URL_PATTERN.search(value):
                    kernel.findings.append(
                        Finding("KMIN-009", rel, pointer, "github.com URL found; live GitHub refs are forbidden in the kernel")
                    )


def _check_actor_safety(kernel: Kernel) -> None:
    modes = {
        entry.get("id"): entry
        for entry in kernel.files.get("execution_modes.json", {}).get("entries", [])
        if isinstance(entry, dict)
    }
    actors = kernel.files.get("actors.json", {}).get("entries", [])
    for index, actor in enumerate(actors):
        if not isinstance(actor, dict):
            continue
        if actor.get("surface") in ("terminal", "human"):
            continue
        pointer = f"/entries/{index}/allowed_mode_refs"
        for mode_ref in actor.get("allowed_mode_refs", []):
            mode = modes.get(mode_ref, {})
            allowed = set(mode.get("allowed_actions", []))
            if allowed & WRITE_CAPABLE_ACTIONS:
                kernel.findings.append(
                    Finding(
                        "KMIN-010",
                        "kernel/actors.json",
                        pointer,
                        f"non-terminal actor '{actor.get('id')}' allows write-capable mode '{mode_ref}'",
                    )
                )


def _check_size_budget(kernel: Kernel) -> None:
    manifest = kernel.files.get("manifest.json", {})
    budget = manifest.get("size_budget", {})
    limit = budget.get("kernel_total_bytes_max")
    if not isinstance(limit, int):
        return
    total = sum(
        (kernel.root / "kernel" / name).stat().st_size
        for name in kernel.files
        if (kernel.root / "kernel" / name).exists()
    )
    if total > limit:
        kernel.findings.append(
            Finding(
                "KMIN-011",
                "kernel/",
                "",
                f"kernel size {total} bytes exceeds the hard budget of {limit} bytes; shrink before adding",
            )
        )


def validate_kernel(root: Path | str) -> list[Finding]:
    kernel = Kernel(root=Path(root))
    _load(kernel)
    if kernel.files:
        _check_manifest(kernel)
        ids = _check_envelopes_and_ids(kernel)
        _check_references(kernel, ids)
        _check_statuses(kernel)
        _check_forbidden_content(kernel)
        _check_actor_safety(kernel)
        _check_size_budget(kernel)
    elif not kernel.findings:
        kernel.findings.append(Finding("KMIN-001", "kernel/", "", "no kernel files found"))
    return kernel.findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="legacy-project-os",
        help="root containing kernel/ (default: legacy-project-os, the archived English kernel)",
    )
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args(argv)
    try:
        findings = validate_kernel(args.root)
    except Exception as exc:  # fail closed on unexpected tooling errors
        print(f"tooling error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    else:
        for finding in findings:
            print(finding.render())
        print(f"kernel validation: {'FAIL' if findings else 'OK'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
