"""Composition-neutral driver for the single wizard transition contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.operation_prompt_wizard_core import (
    OperationTemplate,
    WizardSession,
    generated_filename,
    render_prompt,
    transition_session,
)
from tools.operation_prompt_wizard_filesystem import (
    cleanup_previous_generated_prompts,
    find_replaceable_prompts,
    write_prompt,
)


def run_wizard_session(
    adapter: Any,
    *,
    selection: Any,
    operations: list[OperationTemplate],
    output_directory: Path,
    phase_by_operation: dict[int, str],
    skill_choices: tuple[str, ...],
    skill_options: tuple[Any, ...],
) -> Path | None:
    """Run one adapter through the sole session transition state machine."""

    session = WizardSession()
    while session.stage != "exit":
        if session.stage == "select_operation":
            adapter.show_session(session.current_prompt_path, selection, output_directory)
            operation, captured_intent = adapter.select(operations, phase_by_operation)
            if operation is None:
                session = transition_session(session, "selection_cancel")
                if session.stage == "exit":
                    adapter.say("Cancelled before operation selection. No file was created.")
                continue
            session = transition_session(
                session, "selected", operation=operation, captured_intent=captured_intent
            )
            continue

        if session.stage == "collect_values":
            assert session.operation is not None
            result = adapter.collect_values(
                session.operation, session.values, skill_choices, skill_options
            )
            if result.action == "cancel":
                session = transition_session(session, "values_cancel", values=result.values)
                if session.stage == "exit":
                    adapter.say("Cancelled before write. No file was created.")
                continue
            if result.action == "operation":
                adapter.say("Returning to operation selection.")
                session = transition_session(session, "values_operation", values=result.values)
                continue
            session = transition_session(
                session,
                "values_complete",
                operation=session.operation,
                values=result.values,
            )
            continue

        if session.stage == "route_prompt_path":
            assert session.operation is not None
            result = adapter.choose_route_path(session.operation, session.values)
            if result.action == "cancel":
                session = transition_session(session, "route_cancel", values=result.values)
                if session.stage == "exit":
                    adapter.say("Cancelled before write. No file was created.")
                continue
            if result.action == "values":
                adapter.say("Returning to variable entry.")
                session = transition_session(session, "route_values", values=result.values)
                continue
            session = transition_session(
                session,
                "route_preview",
                values=result.values,
                include_route_prompt_authorization=result.include_pm_authorization_status,
            )
            continue

        if session.stage == "preview":
            assert session.operation is not None
            rendered = render_prompt(
                session.operation,
                session.values,
                include_route_prompt_authorization=session.include_route_prompt_authorization,
            )
            output_path = output_directory / generated_filename(session.operation, rendered)
            replacing = find_replaceable_prompts(output_directory, output_path)
            action = adapter.choose_preview(
                session.operation,
                session.values,
                rendered,
                output_path,
                replacing,
                session.include_route_prompt_authorization,
            )
            if action == "write":
                path = write_prompt(output_path, rendered)
                removed = cleanup_previous_generated_prompts(output_directory, keep_path=path)
                session = transition_session(session, "written", current_prompt_path=path)
                adapter.say(f"Wrote generated prompt: {path}")
                for removed_path in removed:
                    adapter.say(f"Removed previous generated prompt: {removed_path}")
                continue
            if action == "edit":
                adapter.say("Returning to variable entry.")
                session = transition_session(session, "preview_edit")
                continue
            if action == "operation":
                adapter.say("Returning to operation selection.")
                session = transition_session(session, "preview_operation")
                continue
            session = transition_session(session, "preview_cancel")
            if session.stage == "exit":
                adapter.say("Cancelled before write. No file was created.")
            continue

        if session.stage == "post_write":
            assert session.current_prompt_path is not None
            action = adapter.choose_post_write(session.current_prompt_path)
            event = {
                "exit": "post_exit",
                "new": "post_new",
                "same": "post_same",
                "edit": "post_edit",
            }.get(action)
            if event is None:
                raise AssertionError(f"unreachable post-write action: {action!r}")
            if event == "post_exit":
                adapter.say("Exiting wizard session.")
            session = transition_session(session, event)
            continue

        raise AssertionError(f"unreachable wizard stage: {session.stage!r}")

    return session.current_prompt_path
