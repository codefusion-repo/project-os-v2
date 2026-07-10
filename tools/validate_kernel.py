"""Read-only integrity validator for the active ``project-os-es`` kernel.

The validator checks the active Spanish kernel's JSON shape, active ids,
cross-references, template/skill paths, and durable-content safety.  It does
does not validate removed historical surfaces as active routes and grants no
permission.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KERNEL_DIR = REPO_ROOT / "project-os-es" / "kernel"
KERNEL_FILES = {
    "manifest.json": "manifest",
    "reglas-operativas.json": "operational_rules",
    "actores.json": "actors",
    "modos.json": "modes",
    "workflows.json": "workflows",
    "limites.json": "limits",
    "evidencia.json": "evidence",
    "salidas.json": "outputs",
    "artefactos.json": "artefactos",
    "skills.json": "skills",
    "estados.json": "statuses",
}
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


def _load(kernel_dir: Path, findings: list[Finding]) -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    for filename, collection in KERNEL_FILES.items():
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
        data[collection] = [entry for entry in entries if isinstance(entry, dict) and entry.get("active")]
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
    """Validate the active Spanish kernel directory and return all findings."""
    directory = DEFAULT_KERNEL_DIR if kernel_dir is None else Path(kernel_dir)
    findings: list[Finding] = []
    data = _load(directory, findings)
    if findings:
        return findings
    indexes = {collection: _index(data[collection], filename, findings) for filename, collection in KERNEL_FILES.items()}
    manifest = data["manifest"]
    if len(manifest) != 1:
        findings.append(Finding("KES-009", "manifest.json", "exactly one active manifest is required"))
        return findings
    manifest_key = manifest[0].get("key")
    rules = indexes["operational_rules"]
    if not any(rule.get("manifest_key") == manifest_key for rule in rules.values()):
        findings.append(Finding("KES-005", "reglas-operativas.json", "no active rule references the active manifest"))

    actors, modes, workflows = indexes["actors"], indexes["modes"], indexes["workflows"]
    evidence, outputs, statuses = indexes["evidence"], indexes["outputs"], indexes["statuses"]
    for actor in actors.values():
        for mode in actor.get("allowed_modes", []):
            _check_reference(modes, mode, "actores.json", findings)
    for workflow in workflows.values():
        for key in workflow.get("required_evidence", []):
            _check_reference(evidence, key, "workflows.json", findings)
        for key in workflow.get("allowed_outputs", []):
            _check_reference(outputs, key, "workflows.json", findings)
    for limit in data["limits"]:
        if limit.get("actor_key") is not None:
            _check_reference(actors, limit.get("actor_key"), "limites.json", findings)
        _check_reference(statuses, limit.get("on_violation"), "limites.json", findings)
    for item in data["evidence"]:
        _check_reference(statuses, item.get("missing_status"), "evidencia.json", findings)
        for key in item.get("workflow_key", []):
            _check_reference(workflows, key, "evidencia.json", findings)
    for item in data["outputs"]:
        if item.get("status_key") is not None:
            _check_reference(statuses, item.get("status_key"), "salidas.json", findings)
        for key in item.get("workflow_key", []):
            _check_reference(workflows, key, "salidas.json", findings)
    for artifact in data["artefactos"]:
        for key in artifact.get("workflow_key", []):
            _check_reference(workflows, key, "artefactos.json", findings)
        if artifact.get("output_key") is not None:
            _check_reference(outputs, artifact.get("output_key"), "artefactos.json", findings)
        _check_project_markdown(artifact.get("required_template"), ("project-os-es", "templates"), "artefactos.json", directory, findings)
    for skill in data["skills"]:
        _check_project_markdown(skill.get("required_skill"), ("project-os-es", "habilidades"), "skills.json", directory, findings)
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
