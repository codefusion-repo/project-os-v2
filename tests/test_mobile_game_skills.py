"""Focused contracts for the bilingual mobile and game-development skills."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.project_os_resolve import resolve


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
EXPECTED_KEYS = (
    "skill.arquitectura_backend",
    "skill.desarrollo_frontend",
    "skill.desarrollo_mobile",
    "skill.desarrollo_videojuegos",
)
EXPECTED_PATHS = {
    "es": {
        "skill.desarrollo_mobile": "project-os-es/habilidades/desarrollo-mobile.md",
        "skill.desarrollo_videojuegos": "project-os-es/habilidades/desarrollo-videojuegos.md",
    },
    "en": {
        "skill.desarrollo_mobile": "project-os-en/skills/mobile-development.md",
        "skill.desarrollo_videojuegos": "project-os-en/skills/game-development.md",
    },
}
SECTIONS = {
    "es": (
        "## Responsabilidad",
        "## Cuándo conviene usarla",
        "## Criterios de calidad",
        "## Riesgos que debe detectar",
        "## Decisiones que debe favorecer",
        "## Señales de alerta",
        "## Ejemplos de criterio",
        "## Output esperado de la skill",
        "## Límites / no autorización",
    ),
    "en": (
        "## Responsibility",
        "## When to use it",
        "## Quality criteria",
        "## Risks to detect",
        "## Decisions to favor",
        "## Warning signs",
        "## Examples of judgment",
        "## Expected output",
        "## Limits / non-authorization",
    ),
}
TOPICS = {
    ("es", "skill.desarrollo_mobile"): (
        "foreground", "background", "navegación", "offline", "permisos",
        "accesibilidad", "batería", "startup", "hardware", "ios", "android",
        "migraciones locales", "notificaciones", "stores", "hardware físico",
        "privacidad",
    ),
    ("en", "skill.desarrollo_mobile"): (
        "foreground", "background", "navigation", "offline", "permissions",
        "accessibility", "battery", "startup", "hardware", "ios", "android",
        "local persistence", "notifications", "stores", "physical hardware",
        "privacy",
    ),
    ("es", "skill.desarrollo_videojuegos"): (
        "game loop", "frame budget", "input", "escenas", "física", "pooling",
        "asset pipeline", "save/load", "audio", "networking", "plataformas",
        "profiling", "accesibilidad", "hardware real",
    ),
    ("en", "skill.desarrollo_videojuegos"): (
        "game loop", "frame budget", "input", "scenes", "physics", "pooling",
        "asset pipeline", "save/load", "audio", "networking", "platforms",
        "profiling", "accessibility", "real hardware",
    ),
}


def load_skills(kernel_dir: Path) -> list[dict[str, object]]:
    payload = json.loads((kernel_dir / "skills.json").read_text(encoding="utf-8"))
    return [skill for skill in payload["skills"] if skill.get("active")]


@pytest.mark.parametrize(("language", "kernel_dir"), (("es", ES_KERNEL), ("en", EN_KERNEL)))
def test_catalogs_add_exact_domain_keys_with_protected_paths_and_non_authorization(
    language: str, kernel_dir: Path
) -> None:
    skills = load_skills(kernel_dir)
    assert tuple(skill["key"] for skill in skills) == EXPECTED_KEYS

    indexed = {skill["key"]: skill for skill in skills}
    for key, expected_path in EXPECTED_PATHS[language].items():
        skill = indexed[key]
        assert skill["required_skill"] == expected_path
        assert (REPO_ROOT / expected_path).is_file()
        non_authorization = str(skill["non_authorization"]).lower()
        assert ("no concede permisos" if language == "es" else "grants no permission") in non_authorization


@pytest.mark.parametrize(("language", "kernel_dir"), (("es", ES_KERNEL), ("en", EN_KERNEL)))
def test_generic_resolver_selects_only_the_requested_domain_skill(
    language: str, kernel_dir: Path
) -> None:
    baseline = resolve(
        "actor.browser_chat", "workflow.pm_intake", "mode.review_only", kernel_dir=kernel_dir
    )
    assert baseline["estado"] == "status.resolved"
    assert "requested_skills" not in baseline["resuelto"]

    for key, expected_path in EXPECTED_PATHS[language].items():
        result = resolve(
            "actor.browser_chat",
            "workflow.pm_intake",
            "mode.review_only",
            kernel_dir=kernel_dir,
            skill=key,
        )
        assert result["estado"] == "status.resolved"
        assert [item["key"] for item in result["resuelto"]["requested_skills"]] == [key]
        assert result["resuelto"]["requested_skills"][0]["required_skill"] == expected_path


@pytest.mark.parametrize(("language", "key"), tuple(TOPICS))
def test_domain_skill_content_preserves_structure_depth_and_portability(
    language: str, key: str
) -> None:
    path = REPO_ROOT / EXPECTED_PATHS[language][key]
    content = path.read_text(encoding="utf-8")
    lowered = content.lower()

    for section in SECTIONS[language]:
        assert section in content
    for topic in TOPICS[(language, key)]:
        assert topic in lowered
    assert ("Problemático" if language == "es" else "Problematic") in content
    assert ("Mejor" if language == "es" else "Better") in content
    assert "Project OS" in content
    assert "framework" in lowered or "engine" in lowered
