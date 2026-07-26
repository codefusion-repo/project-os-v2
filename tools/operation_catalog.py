"""Canonical operation and alias metadata for the local MOSDLC catalogs.

Operation Markdown remains the single source of truth. Canonical files own the
complete prompt and their alias list; historical alias files are compatibility
stubs that point at one canonical code and never duplicate an operational
contract. This module only reads and validates those local files.
"""

from __future__ import annotations

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
CLASSIFIED_DISTINCT_CONTRACT_GROUPS = frozenset(
    {
        frozenset({"MOS-0.3", "MOS-0.4"}),
        frozenset({"MOS-2.1", "MOS-2.2", "MOS-2.3", "MOS-2.4", "MOS-2.5"}),
        frozenset({"MOS-2.9", "MOS-2.10", "MOS-2.11", "MOS-2.12", "MOS-2.13"}),
        frozenset({"MOS-2.6", "MOS-2.14"}),
        frozenset({"MOS-3.19", "MOS-3.20", "MOS-3.21", "MOS-3.22"}),
        frozenset({"MOS-5.11", "MOS-5.13"}),
        frozenset({"MOS-6.8", "MOS-6.12"}),
        # Distinct lifecycle entry points that share one downstream contract:
        # MOS-3.14 processes a phase-3 audit result, MOS-6.11 a phase-6 code
        # improvement result. Their signatures converged once the derived issue
        # and PR stopped being manual inputs on MOS-3.14; the overlap predates
        # that change and only the redundant metadata was masking it.
        frozenset({"MOS-3.14", "MOS-6.11"}),
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
    explicit: bool = False


@dataclass(frozen=True)
class OperationSource:
    path: Path
    relative_path: str
    code: str
    text: str
    metadata: OperationMetadata

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
        explicit=True,
    )


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
        sources.append(
            OperationSource(
                path=path,
                relative_path=path.relative_to(root).as_posix(),
                code=code,
                text=text,
                metadata=parse_operation_metadata(text, code),
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
        if not metadata.compatibility_reason or not canonical.metadata.compatibility_reason:
            findings.append(OperationCatalogFinding("OPS-013", alias.relative_path, "canonical and alias compatibility reasons are required", "status.blocked"))
        if any(marker in alias.text for marker in ALIAS_CONTRACT_MARKERS):
            findings.append(OperationCatalogFinding("OPS-014", alias.relative_path, "alias stub duplicates operational fields instead of inheriting the canonical prompt", "status.blocked"))

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
        projection_left = (left.canonical_code, left.operation_id, left.aliases, left.alias_of, left.deprecation)
        projection_right = (right.canonical_code, right.operation_id, right.aliases, right.alias_of, right.deprecation)
        if projection_left != projection_right:
            findings.append(OperationCatalogFinding("OPS-018", code, "canonical/alias metadata drift between ES and EN", "status.blocked"))
    return findings
