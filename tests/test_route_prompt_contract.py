"""Behavioral guards for the route-prompt machine block in both languages.

The block is filled by the wizard/browser chat and grepped by the receiving
agent; its shape and machine tokens are executable contract. Prose around the
block stays free to change.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    HYDRATION_LEVEL_CHOICES,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = (
    REPO_ROOT / "project-os-es/templates/route-prompt.md",
    REPO_ROOT / "project-os-en/templates/route-prompt.md",
)
CHANGE_CLASS_KEYS = (
    "change_class.read",
    "change_class.small",
    "change_class.standard",
    "change_class.critical",
)


def prompt_block(template_path: Path) -> str:
    text = template_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, f"{template_path.name} must contain exactly one text block"
    return blocks[0]


def block_lines(template_path: Path) -> list[str]:
    return [line for line in prompt_block(template_path).splitlines() if line.strip()]


@pytest.mark.parametrize("template_path", TEMPLATES)
def test_block_is_one_variable_list_plus_one_final_instruction(template_path: Path) -> None:
    lines = block_lines(template_path)

    assert lines[-1].startswith("{{")
    assert sum(line.startswith("{{") for line in lines) == 1
    for line in lines[:-1]:
        assert " = " in line or line.startswith("recommended_effort:"), line
    assert sum(line.startswith("SCOPE =") for line in lines) == 1
    assert sum(line.startswith("WORK_UNIT =") for line in lines) == 1


@pytest.mark.parametrize("template_path", TEMPLATES)
def test_authorization_tokens_match_the_wizard_machine_values(template_path: Path) -> None:
    lines = block_lines(template_path)
    authorization_line = next(
        line for line in lines if line.startswith("PM_AUTHORIZATION_STATUS =")
    )

    assert PM_AUTHORIZATION_PENDING in authorization_line
    assert PM_AUTHORIZATION_GRANTED in authorization_line

    hydration_line = next(line for line in lines if line.startswith("HYDRATION_LEVEL ="))
    for choice in HYDRATION_LEVEL_CHOICES:
        assert choice in hydration_line


@pytest.mark.parametrize("template_path", TEMPLATES)
def test_change_class_line_enumerates_exactly_the_kernel_classes(template_path: Path) -> None:
    lines = block_lines(template_path)
    change_class_line = next(line for line in lines if line.startswith("CHANGE_CLASS ="))

    assert tuple(re.findall(r"change_class\.[a-z]+", change_class_line)) == CHANGE_CLASS_KEYS


def test_both_languages_declare_the_same_field_sequence() -> None:
    sequences = []
    for template_path in TEMPLATES:
        sequences.append(
            [
                line.split(" = ", 1)[0]
                for line in block_lines(template_path)
                if " = " in line
            ]
        )
    assert sequences[0] == sequences[1]
