"""Pure-contract regression guards for the modular operation prompt wizard."""

from __future__ import annotations

from pathlib import Path
import inspect

import pytest

from tools.operation_prompt_wizard_core import (
    InputVariable,
    OperationTemplate,
    WizardError,
    WizardSession,
    transition_session,
)
from tools.operation_prompt_wizard_filesystem import cleanup_previous_generated_prompts
from tools import operation_prompt_wizard as wizard
from tools import operation_prompt_wizard_line_ui as line_ui
from tools import operation_prompt_wizard_prompt_toolkit_ui as prompt_toolkit_ui
from tools import operation_prompt_wizard_session as session_driver


def route_operation() -> OperationTemplate:
    return OperationTemplate(
        index=1,
        path=Path("MOS-3.5-route.md"),
        title="Route",
        description="Route a request",
        text=(
            "# MOS-3.5 — Route\n\nINPUT:\n  ISSUE_NUMBER=<issue>\n\n"
            "OUTPUT:\n  output.route_prompt\n"
        ),
        variables=(InputVariable("ISSUE_NUMBER", "<issue>", True, "  ISSUE_NUMBER=<issue>"),),
    )


def test_pure_session_transition_contract_covers_shared_navigation_without_effects() -> None:
    operation = route_operation()
    session = transition_session(WizardSession(), "selected", operation=operation)
    assert session.stage == "collect_values"
    assert session.operation == operation

    session = transition_session(
        session, "values_complete", operation=operation, values={"ISSUE_NUMBER": "490"}
    )
    assert session.stage == "preview"
    assert session.values == {"ISSUE_NUMBER": "490"}

    session = transition_session(session, "preview_edit")
    assert session.stage == "collect_values"

    session = transition_session(session, "preview_operation")
    assert session.stage == "select_operation"

    written_path = Path("/tmp/generated.md")
    session = transition_session(session, "written", current_prompt_path=written_path)
    assert session.stage == "post_write"
    assert session.current_prompt_path == written_path
    assert session.written_operation == operation

    session = transition_session(session, "post_same")
    assert session.stage == "collect_values"
    assert session.operation == operation


def test_cleanup_rejects_a_keep_path_outside_the_resolved_output_directory(tmp_path: Path) -> None:
    output_directory = tmp_path / "output"
    output_directory.mkdir()
    outside = tmp_path / "manual.md"
    outside.write_text("manual", encoding="utf-8")

    with pytest.raises(WizardError, match="direct children"):
        cleanup_previous_generated_prompts(output_directory, outside)


def test_only_the_shared_session_driver_owns_wizard_stages() -> None:
    """Adapters render controls; they cannot grow independent state machines."""

    assert "stage ==" in inspect.getsource(session_driver.run_wizard_session)
    assert "stage ==" not in inspect.getsource(line_ui)
    assert "stage ==" not in inspect.getsource(prompt_toolkit_ui)
    prompt_source = inspect.getsource(prompt_toolkit_ui)
    for shared_decision in (
        "line_ui.select_operation",
        "line_ui.collect_values_with_controls",
        "line_ui.collect_route_prompt_path_with_controls",
        "line_ui.choose_preview_action",
        "line_ui.choose_post_write_action",
    ):
        assert shared_decision in prompt_source


def test_programmatic_value_collection_keeps_the_optional_skill_catalog_fallback() -> None:
    operation = OperationTemplate(
        index=1,
        path=Path("MOS-3.1-skill.md"),
        title="Skill",
        description="Select a skill",
        text="",
        variables=(InputVariable("OPTIONAL_SKILL", "<OPTIONAL_SKILL>", False, ""),),
    )

    result = wizard.collect_values(operation, input_func=lambda _prompt: "none")

    assert result == {"OPTIONAL_SKILL": "none"}
