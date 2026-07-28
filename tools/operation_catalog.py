"""Canonical operation and alias metadata for the local MOSDLC catalogs.

Operation Markdown remains the single source of truth. Canonical files own the
complete prompt and their alias list; historical alias files are compatibility
stubs that point at one canonical code and never duplicate an operational
contract. This module only reads and validates those local files.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


METADATA_PATTERN = re.compile(
    r"<!--\s*project-os-operation\s*\n(?P<body>.*?)\n\s*-->", re.DOTALL
)
MOS_CODE_PATTERN = re.compile(r"^(MOS-(?:\d+\.\d+|R\.\d+))(?=-|$)", re.IGNORECASE)
OPERATION_ID_PATTERN = re.compile(
    r"(?:Operaci[oó]n\s+MOSDLC|MOSDLC\s+operation)\s+`(?P<identity>[a-z0-9][a-z0-9-]*)`",
    re.IGNORECASE,
)
ALLOWED_DEPRECATION_STATES = {"none", "supported", "deprecated"}
ALLOWED_ALIAS_FOCUS_AREAS = {"performance", "product", "code_quality"}
ALIAS_CONTRACT_MARKERS = (
    "- Kernel:",
    "- Evidencia:",
    "- Evidence:",
    "- Aprobación PM:",
    "- PM approval:",
    "**Variables**",
    "**Entrega:**",
    "**Deliver:**",
)
SHARED_CONTRACT_ROOT = Path(__file__).resolve().parent.parent / "operation-contracts"
SHARED_CONTRACT_REFERENCE = "shared_contract"
CLASSIFIED_DISTINCT_CONTRACT_GROUPS = frozenset(
    {
        frozenset({"MOS-0.3", "MOS-0.4"}),
        frozenset({"MOS-2.1", "MOS-2.2", "MOS-2.3", "MOS-2.4", "MOS-2.5"}),
        frozenset({"MOS-2.9", "MOS-2.10", "MOS-2.11", "MOS-2.12", "MOS-2.13"}),
        frozenset({"MOS-2.6", "MOS-2.14"}),
        frozenset({"MOS-3.19", "MOS-3.20", "MOS-3.21", "MOS-3.22"}),
        frozenset({"MOS-5.11", "MOS-5.13"}),
        frozenset({"MOS-6.8", "MOS-6.12"}),
    }
)


@dataclass(frozen=True)
class OperationMetadata:
    canonical_code: str
    operation_id: str
    aliases: tuple[str, ...] = ()
    alias_of: str | None = None
    deprecation: str = "none"
    compatibility_reason: str = ""
    alias_focus_area: str = ""
    shared_contract: str = ""
    explicit: bool = False


@dataclass(frozen=True)
class OperationSource:
    path: Path
    relative_path: str
    code: str
    text: str
    metadata: OperationMetadata
    localized_text: str = ""

    @property
    def is_alias(self) -> bool:
        return self.metadata.alias_of is not None


@dataclass(frozen=True)
class OperationContractSignature:
    """Stable contract fields, independent from declared identity and prose."""

    workflows: tuple[str, ...]
    modes: tuple[str, ...]
    outputs: tuple[str, ...]
    evidence: tuple[str, ...]
    approval_required: bool | None
    variables: tuple[tuple[str, bool], ...]
    surface: tuple[str, ...]
    next_operations: tuple[str, ...]


@dataclass(frozen=True)
class OperationCatalogFinding:
    code: str
    path: str
    message: str
    status: str

    def render(self) -> str:
        return f"{self.code} {self.path}: {self.message} ({self.status})"


def _code(value: str) -> str:
    return value.strip().upper()


def _operation_code(path: Path) -> str | None:
    match = MOS_CODE_PATTERN.match(path.stem)
    return _code(match.group(1)) if match else None


def _metadata_values(text: str) -> dict[str, str] | None:
    match = METADATA_PATTERN.search(text)
    if not match:
        return None
    values: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid operation metadata line: {raw_line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key) or key in values:
            raise ValueError(f"invalid or duplicate operation metadata key: {key!r}")
        values[key] = value.strip()
    return values


def parse_operation_metadata(text: str, code: str) -> OperationMetadata:
    """Parse explicit embedded metadata, deriving canonical defaults otherwise."""

    identity_match = OPERATION_ID_PATTERN.search(text)
    derived_identity = identity_match.group("identity") if identity_match else code.lower()
    values = _metadata_values(text)
    if values is None:
        return OperationMetadata(canonical_code=code, operation_id=derived_identity)

    allowed = {
        "canonical_code",
        "operation_id",
        "aliases",
        "alias_of",
        "deprecation",
        "compatibility_reason",
        "alias_focus_area",
        SHARED_CONTRACT_REFERENCE,
    }
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise ValueError(f"unknown operation metadata keys: {', '.join(unknown)}")
    aliases = tuple(_code(item) for item in values.get("aliases", "").split(",") if item.strip())
    alias_of = _code(values["alias_of"]) if values.get("alias_of") else None
    canonical_code = _code(values.get("canonical_code", alias_of or code))
    return OperationMetadata(
        canonical_code=canonical_code,
        operation_id=values.get("operation_id", "" if alias_of else derived_identity),
        aliases=aliases,
        alias_of=alias_of,
        deprecation=values.get("deprecation", "supported" if alias_of else "none").lower(),
        compatibility_reason=values.get("compatibility_reason", ""),
        alias_focus_area=values.get("alias_focus_area", "").lower(),
        shared_contract=values.get(SHARED_CONTRACT_REFERENCE, ""),
        explicit=True,
    )


def _shared_contract_path(key: str) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", key):
        raise ValueError(f"invalid shared operation contract reference: {key!r}")
    return SHARED_CONTRACT_ROOT / f"{key}.json"


def _shared_contract(key: str) -> dict[str, object]:
    path = _shared_contract_path(key)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read shared operation contract {key!r}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"shared operation contract {key!r} must be an object")
    allowed = {"key", "canonical", "aliases"}
    unknown = sorted(set(value) - allowed)
    if unknown or value.get("key") != key:
        raise ValueError(f"invalid shared operation contract {key!r}")
    canonical = value.get("canonical")
    aliases = value.get("aliases")
    if not isinstance(canonical, dict) or not isinstance(aliases, list):
        raise ValueError(f"shared operation contract {key!r} is incomplete")
    required = {
        "code", "operation_id", "aliases", "deprecation", "risk", "surface", "workflow",
        "mode", "outputs", "evidence", "pm_approval", "variables", "connections",
    }
    if set(canonical) != required:
        raise ValueError(f"shared operation contract {key!r} has unknown or missing canonical fields")
    if not all(isinstance(canonical[name], str) for name in ("code", "operation_id", "deprecation", "risk", "surface", "workflow", "mode", "pm_approval")):
        raise ValueError(f"shared operation contract {key!r} has invalid canonical values")
    if not all(isinstance(canonical[name], list) for name in ("aliases", "outputs", "evidence", "variables", "connections")):
        raise ValueError(f"shared operation contract {key!r} has invalid canonical lists")
    if canonical["deprecation"] not in ALLOWED_DEPRECATION_STATES:
        raise ValueError(f"shared operation contract {key!r} has invalid deprecation")
    if canonical["risk"] not in {"low", "medium", "high", "critical"} or canonical["surface"] not in {"browser_chat", "terminal_agent", "human_pm"}:
        raise ValueError(f"shared operation contract {key!r} has invalid risk or surface")
    if canonical["pm_approval"] not in {"not_required", "required"}:
        raise ValueError(f"shared operation contract {key!r} has invalid approval")
    if not all(isinstance(item, str) for name in ("aliases", "outputs", "evidence", "connections") for item in canonical[name]):
        raise ValueError(f"shared operation contract {key!r} has non-string references")
    if not all(isinstance(item, dict) and set(item) == {"name", "required", "placeholder"} and isinstance(item["name"], str) and isinstance(item["required"], bool) and isinstance(item["placeholder"], str) for item in canonical["variables"]):
        raise ValueError(f"shared operation contract {key!r} has invalid variables")
    variable_names = [item["name"] for item in canonical["variables"]]
    if len(set(variable_names)) != len(variable_names):
        raise ValueError(f"shared operation contract {key!r} has duplicate variables")
    alias_codes: list[str] = []
    for alias in aliases:
        if not isinstance(alias, dict) or set(alias) != {"code", "alias_of", "deprecation", "alias_focus_area"}:
            raise ValueError(f"shared operation contract {key!r} has invalid alias fields")
        if not all(isinstance(alias[name], str) for name in alias):
            raise ValueError(f"shared operation contract {key!r} has invalid alias values")
        if alias["alias_of"] != canonical["code"] or alias["deprecation"] not in {"supported", "deprecated"}:
            raise ValueError(f"shared operation contract {key!r} has an invalid alias relation")
        if alias["alias_focus_area"] not in ALLOWED_ALIAS_FOCUS_AREAS:
            raise ValueError(f"shared operation contract {key!r} has an invalid alias focus area")
        alias_codes.append(alias["code"])
    if len(set(alias_codes)) != len(alias_codes) or tuple(alias_codes) != tuple(canonical["aliases"]):
        raise ValueError(f"shared operation contract {key!r} has ambiguous aliases")
    focus = next((item for item in canonical["variables"] if item["name"] == "FOCUS_AREA"), None)
    if not {"FOCUS_AREA", "TARGET_REPOSITORY"} <= set(variable_names) or not isinstance(focus, dict) or focus["placeholder"] != "<performance|product|code_quality>":
        raise ValueError(f"shared operation contract {key!r} has incompatible variables")
    _validate_shared_references(key, canonical)
    return value


def _validate_shared_references(key: str, canonical: dict[str, object]) -> None:
    """Validate only references that are machine identifiers against the active kernel."""

    kernel_root = Path(__file__).resolve().parent.parent / "project-os-es" / "kernel"
    collections = {
        "workflow": ("workflows.json", "workflows"),
        "mode": ("modos.json", "modes"),
        "output": ("salidas.json", "outputs"),
        "evidence": ("evidencia.json", "evidence"),
    }
    known: dict[str, set[str]] = {}
    for kind, (filename, collection) in collections.items():
        try:
            payload = json.loads((kernel_root / filename).read_text(encoding="utf-8"))
            known[kind] = {item["key"] for item in payload[collection] if isinstance(item, dict) and isinstance(item.get("key"), str)}
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot validate shared operation contract {key!r} references: {exc}") from exc
    references = {
        "workflow": [canonical["workflow"]],
        "mode": [canonical["mode"]],
        "output": canonical["outputs"],
        "evidence": canonical["evidence"],
    }
    for kind, values in references.items():
        if any(not isinstance(value, str) or value not in known[kind] for value in values):
            raise ValueError(f"shared operation contract {key!r} references an unknown {kind}")


def _localized_compatibility_reason(text: str) -> str:
    match = re.search(r"^\*\*(?:Compatibilidad|Compatibility):\*\*\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _shared_metadata(key: str, code: str, localized_text: str) -> tuple[OperationMetadata, str]:
    contract = _shared_contract(key)
    canonical = contract["canonical"]
    assert isinstance(canonical, dict)
    aliases = contract["aliases"]
    assert isinstance(aliases, list)
    # The language comes from the Markdown labels below; the descriptor contains no prose.
    is_english = "MOSDLC operation" in localized_text or "**Does:**" in localized_text
    labels = {
        "surface": "Surface" if is_english else "Superficie",
        "approval": "PM approval" if is_english else "Aprobación PM",
        "required": "Required" if is_english else "Requeridas",
        "optional": "Optional" if is_english else "Opcionales",
        "deliver": "Deliver" if is_english else "Entrega",
        "connections": "Connections" if is_english else "Conexiones",
    }
    canonical_code = str(canonical["code"])
    compatibility_reason = _localized_compatibility_reason(localized_text)
    if code == canonical_code:
        metadata = OperationMetadata(
            canonical_code=canonical_code,
            operation_id=str(canonical["operation_id"]),
            aliases=tuple(str(item) for item in canonical["aliases"]),
            deprecation=str(canonical["deprecation"]),
            compatibility_reason=compatibility_reason,
            shared_contract=key,
            explicit=True,
        )
        required = [item for item in canonical["variables"] if item["required"]]
        optional = [item for item in canonical["variables"] if not item["required"]]
        inputs = "\n".join(f"  {item['name']}={item['placeholder']}{'' if item['required'] else ' optional'}" for item in canonical["variables"])
        outputs = tuple(str(item) for item in canonical["outputs"])
        output_summary = outputs[0] if len(outputs) == 1 else f"{outputs[0]} (+{' + '.join(outputs[1:])})"
        composed = "\n".join((
            f"MOSDLC operation `{canonical['operation_id']}` · Risk: {canonical['risk']}.",
            f"- {labels['surface']}: {canonical['surface']}",
            f"- Kernel: {canonical['workflow']} · {canonical['mode']} · {output_summary}",
            f"- Evidence: {' · '.join(canonical['evidence'])}",
            f"- {labels['approval']}: {'No' if canonical['pm_approval'] == 'not_required' else 'Yes'}",
            "",
            "**Variables**",
            f"- {labels['required']}: {', '.join(item['name'] for item in required)}",
            f"- {labels['optional']}: {', '.join(item['name'] for item in optional)}",
            "",
            "INPUT:",
            inputs,
            "",
            f"**{labels['deliver']}:** {output_summary}",
            f"**{labels['connections']}:** {'; '.join(canonical['connections'])}",
            "",
            localized_text,
        ))
        return metadata, composed
    matched = [item for item in aliases if isinstance(item, dict) and item.get("code") == code]
    if len(matched) != 1:
        raise ValueError(f"shared operation contract {key!r} does not define {code}")
    alias = matched[0]
    return OperationMetadata(
        canonical_code=canonical_code,
        operation_id="",
        alias_of=str(alias["alias_of"]),
        deprecation=str(alias["deprecation"]),
        compatibility_reason=compatibility_reason,
        alias_focus_area=str(alias["alias_focus_area"]),
        shared_contract=key,
        explicit=True,
    ), localized_text


def load_operation_sources(operations_dir: Path) -> list[OperationSource]:
    """Read one local catalog deterministically without resolving any operation."""

    root = operations_dir.expanduser()
    if not root.is_dir():
        raise ValueError(f"operations directory not found: {root}")
    sources: list[OperationSource] = []
    for path in sorted(root.rglob("*.md"), key=lambda item: item.relative_to(root).as_posix()):
        if path.name == "README.md":
            continue
        code = _operation_code(path)
        if code is None:
            raise ValueError(f"operation filename has no MOS code: {path.relative_to(root)}")
        text = path.read_text(encoding="utf-8")
        metadata = parse_operation_metadata(text, code)
        composed_text = text
        if metadata.shared_contract:
            metadata, composed_text = _shared_metadata(metadata.shared_contract, code, text)
        sources.append(
            OperationSource(
                path=path,
                relative_path=path.relative_to(root).as_posix(),
                code=code,
                text=composed_text,
                metadata=metadata,
                localized_text=text,
            )
        )
    if not sources:
        raise ValueError(f"no .md operation templates found in: {root}")
    return sources


def _refs(text: str, prefix: str) -> tuple[str, ...]:
    return tuple(sorted(set(re.findall(rf"\b{re.escape(prefix)}\.[a-z0-9_.-]+", text))))


def _approval_required(text: str) -> bool | None:
    match = re.search(r"^- (?:Aprobación PM|PM approval):\s*(\S+)", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).lower().rstrip(".,")
    if value in {"sí", "si", "yes"}:
        return True
    if value in {"no"}:
        return False
    return None


def _variables(text: str) -> tuple[tuple[str, bool], ...]:
    match = re.search(r"\*\*Variables\*\*(.*?)(?:\n\s*\n\*\*|\Z)", text, re.DOTALL)
    if not match:
        return ()
    section = match.group(1)
    variables: dict[str, bool] = {}
    for labels, required in (("Requeridas|Required", True), ("Opcionales|Optional", False)):
        line = re.search(rf"^- (?:{labels}):\s*(.+)$", section, re.MULTILINE | re.IGNORECASE)
        if line:
            for name in re.findall(r"\b[A-Z][A-Z0-9_]+\b", line.group(1).split("(", 1)[0]):
                variables[name] = required
    return tuple(sorted(variables.items()))


def _surface(text: str) -> tuple[str, ...]:
    match = re.search(r"^- (?:Superficie|Surface):\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ()
    value = match.group(1).lower()
    known = re.findall(r"\b(?:browser_chat|terminal_agent|human_pm)\b", value)
    if "destinatario externo" in value or "external recipient" in value:
        known.append("external_recipient")
    return tuple(known)


def _next_operations(text: str) -> tuple[str, ...]:
    match = re.search(r"\*\*(?:Conexiones|Connections):\*\*\s*(.+)$", text, re.MULTILINE)
    if not match:
        return ()
    connections = match.group(1)
    parts = re.split(r"\b(?:Después|Next|Recomendada|Recommended):", connections, flags=re.IGNORECASE)
    if len(parts) < 2:
        return ()
    return tuple(_code(item) for item in re.findall(r"MOS-(?:\d+\.\d+|R\.\d+)", " ".join(parts[1:]), re.IGNORECASE))


def operation_contract_signature(source: OperationSource) -> OperationContractSignature:
    return OperationContractSignature(
        workflows=_refs(source.text, "workflow"),
        modes=_refs(source.text, "mode"),
        outputs=_refs(source.text, "output"),
        evidence=_refs(source.text, "evidence"),
        approval_required=_approval_required(source.text),
        variables=_variables(source.text),
        surface=_surface(source.text),
        next_operations=_next_operations(source.text),
    )


def validate_operation_catalog(sources: list[OperationSource]) -> list[OperationCatalogFinding]:
    """Validate aliases and deterministic duplicate identities for one surface."""

    findings: list[OperationCatalogFinding] = []
    by_code: dict[str, list[OperationSource]] = {}
    for source in sources:
        by_code.setdefault(source.code, []).append(source)
        if source.metadata.deprecation not in ALLOWED_DEPRECATION_STATES:
            findings.append(OperationCatalogFinding("OPS-001", source.relative_path, "unknown deprecation state", "status.blocked"))
    for code, matches in by_code.items():
        if len(matches) > 1:
            findings.append(OperationCatalogFinding("OPS-002", code, "ambiguous MOS code", "status.needs_pm_decision"))

    unique = {code: matches[0] for code, matches in by_code.items() if len(matches) == 1}
    canonicals = [source for source in sources if not source.is_alias]
    for source in canonicals:
        metadata = source.metadata
        if metadata.canonical_code != source.code:
            findings.append(OperationCatalogFinding("OPS-003", source.relative_path, "canonical_code must match the canonical filename code", "status.blocked"))
        if not metadata.operation_id:
            findings.append(OperationCatalogFinding("OPS-004", source.relative_path, "canonical operation identity is missing", "status.needs_pm_decision"))
        if metadata.alias_focus_area:
            findings.append(OperationCatalogFinding("OPS-019", source.relative_path, "canonical operations cannot bind an alias focus area", "status.blocked"))
        if len(set(metadata.aliases)) != len(metadata.aliases) or source.code in metadata.aliases:
            findings.append(OperationCatalogFinding("OPS-005", source.relative_path, "canonical aliases are duplicated or self-referential", "status.blocked"))
        for alias_code in metadata.aliases:
            alias = unique.get(alias_code)
            if alias is None or alias.metadata.alias_of != source.code:
                findings.append(OperationCatalogFinding("OPS-006", source.relative_path, f"alias {alias_code} is missing, ambiguous, or does not point back", "status.blocked"))

    for alias in (source for source in sources if source.is_alias):
        metadata = alias.metadata
        canonical = unique.get(metadata.alias_of or "")
        if canonical is None:
            findings.append(OperationCatalogFinding("OPS-007", alias.relative_path, "alias target is missing or ambiguous", "status.blocked"))
            continue
        if canonical.is_alias:
            findings.append(OperationCatalogFinding("OPS-008", alias.relative_path, "alias chains and cycles are forbidden", "status.blocked"))
        if alias.code not in canonical.metadata.aliases:
            findings.append(OperationCatalogFinding("OPS-009", alias.relative_path, "alias is not declared by its canonical operation", "status.blocked"))
        if metadata.canonical_code != metadata.alias_of:
            findings.append(OperationCatalogFinding("OPS-010", alias.relative_path, "alias canonical_code and alias_of differ", "status.blocked"))
        if metadata.aliases or metadata.operation_id:
            findings.append(OperationCatalogFinding("OPS-011", alias.relative_path, "alias stub must not define an identity or child aliases", "status.blocked"))
        if metadata.deprecation not in {"supported", "deprecated"}:
            findings.append(OperationCatalogFinding("OPS-012", alias.relative_path, "alias must declare supported or deprecated status", "status.blocked"))
        if not metadata.compatibility_reason or (
            not canonical.metadata.compatibility_reason and not canonical.metadata.shared_contract
        ):
            findings.append(OperationCatalogFinding("OPS-013", alias.relative_path, "canonical and alias compatibility reasons are required", "status.blocked"))
        if metadata.alias_focus_area and metadata.alias_focus_area not in ALLOWED_ALIAS_FOCUS_AREAS:
            findings.append(OperationCatalogFinding("OPS-020", alias.relative_path, "alias focus area is not allowlisted", "status.blocked"))
        if metadata.alias_focus_area and "FOCUS_AREA" not in dict(_variables(canonical.text)):
            findings.append(OperationCatalogFinding("OPS-021", alias.relative_path, "alias focus area requires FOCUS_AREA on its canonical contract", "status.blocked"))
        if any(marker in alias.text for marker in ALIAS_CONTRACT_MARKERS):
            findings.append(OperationCatalogFinding("OPS-014", alias.relative_path, "alias stub duplicates operational fields instead of inheriting the canonical prompt", "status.blocked"))

    for source in (item for item in canonicals if item.metadata.shared_contract):
        contract = _shared_contract(source.metadata.shared_contract)
        canonical = contract["canonical"]
        assert isinstance(canonical, dict)
        unknown_connections = [
            str(code) for code in canonical["connections"] if str(code) not in unique
        ]
        if unknown_connections:
            findings.append(OperationCatalogFinding("OPS-022", source.relative_path, "shared contract has unknown connections: " + ", ".join(unknown_connections), "status.blocked"))

    identities: dict[str, list[OperationSource]] = {}
    signatures: dict[OperationContractSignature, list[OperationSource]] = {}
    for source in canonicals:
        identities.setdefault(source.metadata.operation_id, []).append(source)
        signatures.setdefault(operation_contract_signature(source), []).append(source)
    for identity, matches in identities.items():
        if identity and len(matches) > 1:
            paths = ", ".join(item.relative_path for item in matches)
            findings.append(OperationCatalogFinding("OPS-015", paths, f"multiple canonical operations claim identity {identity!r}", "status.needs_pm_decision"))
    for signature, matches in signatures.items():
        classified_codes = frozenset(item.code for item in matches)
        if (
            len(matches) > 1
            and classified_codes not in CLASSIFIED_DISTINCT_CONTRACT_GROUPS
        ):
            paths = ", ".join(item.relative_path for item in matches)
            findings.append(OperationCatalogFinding("OPS-016", paths, "undeclared contractual duplicate candidates; PM classification is required", "status.needs_pm_decision"))
    return findings

def validate_bilingual_alias_parity(
    spanish_sources: list[OperationSource], english_sources: list[OperationSource]
) -> list[OperationCatalogFinding]:
    """Compare only stable alias metadata; localized prose remains free to differ."""

    findings: list[OperationCatalogFinding] = []
    es = {source.code: source for source in spanish_sources}
    en = {source.code: source for source in english_sources}
    if set(es) != set(en):
        findings.append(OperationCatalogFinding("OPS-017", "project-os-es/project-os-en", "operation code sets differ", "status.blocked"))
        return findings
    for code in sorted(es):
        left = es[code].metadata
        right = en[code].metadata
        projection_left = (left.canonical_code, left.operation_id, left.aliases, left.alias_of, left.deprecation, left.alias_focus_area)
        projection_right = (right.canonical_code, right.operation_id, right.aliases, right.alias_of, right.deprecation, right.alias_focus_area)
        if projection_left != projection_right:
            findings.append(OperationCatalogFinding("OPS-018", code, "canonical/alias metadata drift between ES and EN", "status.blocked"))
    return findings
