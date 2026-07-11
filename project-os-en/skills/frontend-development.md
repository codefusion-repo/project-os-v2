# Skill: frontend development

## Responsibility

Apply frontend judgment to implementable UI, accessibility, web performance, components, state, and API integration while preserving the live issue scope.

## When to use it

Use for web interfaces, components, client state, forms, responsive behavior, accessibility, browser/editor integration, rendering performance, or API-facing UI. Do not select it for documentation-only wording changes.

## Quality criteria

- Model loading, empty, success, partial, error, offline, disabled, and permission-denied states explicitly where relevant.
- Prefer semantic HTML, keyboard operation, visible focus, correct labels, announcements, contrast, reduced motion, and touch targets.
- Keep server, URL, form, and client state ownership explicit; avoid duplicated or contradictory sources of truth.
- Make destructive actions deliberate and prevent double submission or stale responses.
- Bound rendering and network work; measure before adding memoization, virtualization, or prefetching.
- Preserve responsive layout, localization growth, and resilient content behavior.

## Risks to detect

Clickable non-controls, inaccessible dialogs, focus loss, stale async updates, optimistic-state drift, hydration mismatch, uncontrolled bundle growth, brittle pixel assumptions, hidden errors, secret exposure, and UI-only authorization.

## Decisions to favor

Prefer native semantics, progressive enhancement, explicit state machines where complexity warrants them, colocated component responsibilities, abortable requests, stable API contracts, and user-visible recovery paths.

## Examples of judgment

### All states, not only success

Render a stable container with intentional loading, empty, error, and retry behavior. Preserve the previous result only when the product decision explicitly calls for stale-while-refresh.

### Native semantics before clickable divs

Use `button`, `a`, labels, fieldsets, and dialog semantics before recreating keyboard and accessibility behavior by hand.

### Double submit and destructive action

Disable or serialize duplicate submissions, use an idempotent backend contract where writes may retry, communicate progress, and require a proportionate confirmation for irreversible actions.

## Expected output

Return scoped recommendations or findings with evidence, states, accessibility/performance impacts, validation, risks, and the safe next step. Do not turn the skill into workflow logic.

## Limits / non-authorization

This skill is optional. It grants no permission and never replaces live scope, PM approval, branch preflight, evidence, validation, traceability, or review-before-close.
