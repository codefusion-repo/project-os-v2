# MOS-R.2 — Recommend next operation

MOSDLC operation `recommend-next-operation` · Cross-phase · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only routing; does not authorize the selected operation)

**Does:** Recommend exactly one next MOSDLC operation from live traceability.
**For:** To choose lifecycle path without ad hoc reasoning.
**How:** Read live status, justify the recommendation and show safe alternatives if there is ambiguity.

**Variables**
- Required: — (none)
- Optional: ROUTING_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the repository, the issue, the PR, the roadmap, and the
current status are derived metadata, not inputs. Apply the common contract's
precedence: reuse the unambiguous source the current invocation already
identifies; if none exists, ask for a single `ROUTING_SOURCE` —repository,
issue, PR, roadmap, or equivalent live record— and reconstruct the rest from
it. Return the decision to the PM only on real material ambiguity, never
because a reconstructible identifier is missing.

**Deliver:** output.status_result. In the event of insufficient or unreadable traceability, fail closed: report with `output.status_result` and return the decision to the PM.

**Intent-first continuation:** When the PM seeks an outcome and the route is
unambiguous, do not stop at the recommendation: re-resolve the kernel for the
selected operation, retain its actor, workflow, mode, evidence, and validation
gates, open its template, and produce its next read-only or draft-only output
in the same response. That output belongs to the selected operation, not the
routing workflow. Briefly explain the route within the shape its template
allows, without another MOS selection, mechanical confirmation, or derivable
metadata request. If the PM only asks to recommend or compare routes, deliver
the recommendation without continuing.

To implement a sufficient live unit, continue to MOS-3.4. If the class requires
a formal unit that does not yet exist, draft exactly one through MOS-3.1 or
MOS-3.8 according to its source basis and stop at human creation; a draft is not
a created formal unit. Once that creation result is verifiable, resume MOS-3.4
with the same intent and reference, without asking for the number again or
creating another unit. Do not chain operations beyond the next useful artifact
or cross a material decision or surface boundary. Each continuation requires
its own operation's evidence: resolved routing does not prove that evidence
is complete.

Use available connected read sources to verify the reference and its relations.
If unavailable, apply the common equivalent-source and fail-closed contract;
never invent metadata or ask the PM to transcribe accessible data. Preserve
intent, constraints, and explicit overrides in the chain's context without
persisting state. Continuation never creates authorization or executes writes;
MOS-3.4 retains its exact PM delivery requirement.

**Connections:** Previous: any operation that requires routing. Next: the selected operation, re-resolved under its own gates when continuation applies. Recommended: The selected operation.
