"""Allowed Project OS language surfaces shared by read-only tooling.

This module describes repository paths and JSON collection names. It does not
resolve kernel behavior, select permissions, or authorize any action.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class ProjectOSSurface:
    language: str
    root_name: str
    kernel_files: dict[str, tuple[str, str]]
    templates_name: str
    skills_name: str
    operations_name: str
    authorization_notice: str
    messages: dict[str, str]

    @property
    def root(self) -> Path:
        return REPO_ROOT / self.root_name

    @property
    def kernel_dir(self) -> Path:
        return self.root / "kernel"

    @property
    def operations_dir(self) -> Path:
        return self.root / self.operations_name

    @property
    def skills_catalog_path(self) -> Path:
        return self.kernel_dir / "skills.json"

    @property
    def templates_prefix(self) -> tuple[str, ...]:
        return (self.root_name, self.templates_name)

    @property
    def skills_prefix(self) -> tuple[str, ...]:
        return (self.root_name, self.skills_name)


SPANISH_KERNEL_FILES = {
    "manifest": ("manifest.json", "manifest"),
    "operational_rules": ("reglas-operativas.json", "operational_rules"),
    "actors": ("actores.json", "actors"),
    "modes": ("modos.json", "modes"),
    "workflows": ("workflows.json", "workflows"),
    "limits": ("limites.json", "limits"),
    "evidence": ("evidencia.json", "evidence"),
    "outputs": ("salidas.json", "outputs"),
    "artifacts": ("artefactos.json", "artefactos"),
    "skills": ("skills.json", "skills"),
    "statuses": ("estados.json", "statuses"),
}

ENGLISH_KERNEL_FILES = {
    "manifest": ("manifest.json", "manifest"),
    "operational_rules": ("operational-rules.json", "operational_rules"),
    "actors": ("actors.json", "actors"),
    "modes": ("modes.json", "modes"),
    "workflows": ("workflows.json", "workflows"),
    "limits": ("limits.json", "limits"),
    "evidence": ("evidence.json", "evidence"),
    "outputs": ("outputs.json", "outputs"),
    "artifacts": ("artifacts.json", "artifacts"),
    "skills": ("skills.json", "skills"),
    "statuses": ("statuses.json", "statuses"),
}

SURFACES = (
    ProjectOSSurface(
        language="es",
        root_name="project-os-es",
        kernel_files=SPANISH_KERNEL_FILES,
        templates_name="templates",
        skills_name="habilidades",
        operations_name="operaciones",
        authorization_notice=(
            "Esta resolucion da forma operativa y nunca concede permisos; la autoridad "
            "requiere aprobacion PM exacta y los gates del kernel."
        ),
        messages={
            "missing_file": "archivo del kernel faltante",
            "invalid_file": "archivo del kernel ilegible o invalido",
            "missing_collection": "no contiene la lista",
            "unknown_actor": "actor desconocido",
            "unknown_mode": "mode desconocido",
            "unknown_workflow": "workflow desconocido",
            "unknown_skill": "skill desconocido",
            "known": "conocidos",
            "incompatible_mode": "mode incompatible",
            "missing_template": "template requerido por artefacto no encontrado",
            "missing_skill_file": "skill requerido no encontrado",
            "missing_kernel_dir": "directorio del kernel no encontrado",
            "invalid_kernel_dir": "superficie de kernel no permitida",
            "unexpected_error": "error de tooling inesperado",
        },
    ),
    ProjectOSSurface(
        language="en",
        root_name="project-os-en",
        kernel_files=ENGLISH_KERNEL_FILES,
        templates_name="templates",
        skills_name="skills",
        operations_name="operations",
        authorization_notice=(
            "This resolution provides operating guidance and never grants permission; "
            "authority requires exact PM approval and the kernel gates."
        ),
        messages={
            "missing_file": "missing kernel file",
            "invalid_file": "unreadable or invalid kernel file",
            "missing_collection": "does not contain list",
            "unknown_actor": "unknown actor",
            "unknown_mode": "unknown mode",
            "unknown_workflow": "unknown workflow",
            "unknown_skill": "unknown skill",
            "known": "known",
            "incompatible_mode": "incompatible mode",
            "missing_template": "artifact required template not found",
            "missing_skill_file": "required skill file not found",
            "missing_kernel_dir": "kernel directory not found",
            "invalid_kernel_dir": "kernel surface is not allowed",
            "unexpected_error": "unexpected tooling error",
        },
    ),
)

DEFAULT_SURFACE = SURFACES[0]
DEFAULT_KERNEL_DIR = DEFAULT_SURFACE.kernel_dir


def select_surface(kernel_dir: Path | str | None) -> tuple[ProjectOSSurface | None, Path]:
    """Return the exact allowed surface for ``kernel_dir`` without fallbacks."""

    if kernel_dir is None:
        return DEFAULT_SURFACE, DEFAULT_KERNEL_DIR
    supplied = Path(kernel_dir).expanduser()
    directory = supplied if supplied.is_absolute() else Path.cwd() / supplied
    for surface in SURFACES:
        if directory == surface.kernel_dir:
            return surface, directory
    return None, directory


def surface_for_language(language: str) -> ProjectOSSurface | None:
    """Return the exact allowed surface for a session language, or ``None``."""

    for surface in SURFACES:
        if surface.language == language:
            return surface
    return None


def surface_for_operations_dir(operations_dir: Path | str) -> ProjectOSSurface | None:
    """Return the exact allowed surface owning ``operations_dir``, without fallbacks."""

    supplied = Path(operations_dir).expanduser()
    directory = supplied if supplied.is_absolute() else Path.cwd() / supplied
    for surface in SURFACES:
        if directory == surface.operations_dir or directory.resolve() == surface.operations_dir:
            return surface
    return None
