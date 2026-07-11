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
) -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
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
