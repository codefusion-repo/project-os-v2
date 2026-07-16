"""Stable guards for the final (v3) internal handoff documentation."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_PATH = REPO_ROOT / "docs/decisions/0005-public-repository-strategy.md"
HANDOFF_PATH = REPO_ROOT / "docs/release/INTERNAL_HANDOFF_READINESS.md"

TAG_V1 = "project-os-internal-handoff-v1"
TAG_V2 = "project-os-internal-handoff-v2"
TAG_V3 = "project-os-internal-handoff-v3"

V1_TAG_OBJECT_SHA = "901676d358d37423d8a64896f278075469deb2e8"
V1_COMMIT_SHA = "8b01e9f45b1c2449c9cc799d51ee300b6793e9dc"
V2_TAG_OBJECT_SHA = "e9bafbf1b088e9973bd0dc6e5781415ccc09e000"
V2_COMMIT_SHA = "57c6b5176cc43606191418faf884915888cd9202"
HISTORICAL_SHAS = {
    V1_TAG_OBJECT_SHA,
    V1_COMMIT_SHA,
    V2_TAG_OBJECT_SHA,
    V2_COMMIT_SHA,
}

ISSUE_424 = "https://github.com/codefusion-repo/project-os-v2/issues/424"
ISSUE_438 = "https://github.com/codefusion-repo/project-os-v2/issues/438"
V1_TAG_DECISION_URL = f"{ISSUE_424}#issuecomment-4976581909"
V1_RELEASE_DECISION_URL = f"{ISSUE_424}#issuecomment-4987453334"
V2_DIRECTION_URL = f"{ISSUE_424}#issuecomment-4987758661"
V2_APPROVAL_URL = f"{ISSUE_424}#issuecomment-4987814297"

AMENDMENT_1_HEADING = (
    "## Amendment 1 — bounded internal handoff tag exception (issue #424)"
)
AMENDMENT_2_HEADING = (
    "## Amendment 2 — exact internal GitHub Release for the fixed handoff "
    "baseline (issue #424)"
)
AMENDMENT_3_HEADING = (
    "## Amendment 3 — final internal handoff marker v3 (issue #438)"
)
AMENDMENT_3_ANCHOR = "#amendment-3--final-internal-handoff-marker-v3-issue-438"

V3_RELEASE_TITLE = "Project OS final internal handoff baseline v3"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_adr_preserves_amendments_1_and_2_as_history() -> None:
    text = ADR_PATH.read_text(encoding="utf-8")

    assert AMENDMENT_1_HEADING in text
    assert AMENDMENT_2_HEADING in text
    assert "supersedes the earlier tag-only exclusion and no other action" in text
    assert "They are not retroactively rewritten" in text
    assert TAG_V1 in text
    assert V1_COMMIT_SHA in text
    assert V1_RELEASE_DECISION_URL in text
    assert "2026-07-15T03:30:23Z" in text
    assert "2026-07-16T02:14:10Z" in text
    for preserved_boundary in (
        "does not authorize a visibility or settings change",
        "does not close issue #424 or roadmap #274",
        "the sole source of truth for future Project OS development",
    ):
        assert preserved_boundary in text


def test_adr_amendment_3_defines_the_final_v3_contract() -> None:
    text = ADR_PATH.read_text(encoding="utf-8")
    flat = normalized(ADR_PATH)

    assert AMENDMENT_3_HEADING in text
    assert TAG_V3 in text
    assert V3_RELEASE_TITLE in flat
    assert "an **annotated** git tag (never lightweight)" in flat
    assert "draft `false`, prerelease `false`" in flat
    assert "The SHA is never fixed in advance" in flat
    assert (
        "documentation → validation → merge → post-merge SHA "
        "→ annotated tag → internal Release"
    ) in flat
    assert (
        "Creating `v3` before the documentary merge would fix an incomplete "
        "baseline again and is prohibited."
    ) in flat


def test_adr_records_v1_and_v2_history_with_exact_live_evidence() -> None:
    text = ADR_PATH.read_text(encoding="utf-8")
    flat = normalized(ADR_PATH)

    assert TAG_V1 in text and TAG_V2 in text
    for sha in HISTORICAL_SHAS:
        assert sha in text
    for decision_url in (
        V1_TAG_DECISION_URL,
        V1_RELEASE_DECISION_URL,
        V2_DIRECTION_URL,
        V2_APPROVAL_URL,
        ISSUE_438,
    ):
        assert decision_url in text
    assert "2026-07-16T03:08:14Z" in text
    assert "2026-07-16T03:19:20Z" in text
    assert (
        "moved, reused, replaced, edited, deleted or retroactively "
        "reinterpreted"
    ) in flat
    assert (
        "After issue #438 completes, neither `v1` nor `v2` is the final "
        "baseline; both remain history."
    ) in flat


def test_adr_bounds_supersession_and_declares_finality() -> None:
    flat = normalized(ADR_PATH)

    assert (
        "supersedes `v1` and `v2` **only** as the identity of the final "
        "internal handoff marker"
    ) in flat
    assert (
        "applies exclusively to the new internal tag and its internal Release"
    ) in flat
    assert (
        "no boundary on publication, visibility, settings, archival, creation "
        "of `agent-os-cli`, content transition, CLI implementation, "
        "synchronization or backports is relaxed"
    ) in flat
    assert (
        'There will be no `v4` and no later "finalization" follow-up'
    ) in flat
    assert "it authorizes nothing" in flat


def test_adr_fixes_no_v3_sha_in_advance() -> None:
    text = ADR_PATH.read_text(encoding="utf-8")

    assert set(re.findall(r"\b[0-9a-f]{40}\b", text)) == HISTORICAL_SHAS
    for line in text.splitlines():
        if TAG_V3 in line or "v3" in line.split("`"):
            assert not re.search(r"\b[0-9a-f]{40}\b", line)


def test_handoff_describes_v1_and_v2_as_verified_history() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    flat = normalized(HANDOFF_PATH)

    assert TAG_V1 in text and TAG_V2 in text
    for sha in HISTORICAL_SHAS:
        assert sha in text
    assert "Project OS internal handoff baseline" in text
    assert "Project OS final internal handoff baseline" in text
    for decision_url in (
        V1_TAG_DECISION_URL,
        V1_RELEASE_DECISION_URL,
        V2_DIRECTION_URL,
        V2_APPROVAL_URL,
    ):
        assert decision_url in text
    assert (
        "ninguno de los dos representa el baseline final: no se presentan "
        "como identidad final del handoff"
    ) in flat
    assert "head permanentemente actual de `main`" in flat
    assert "no se congelan en este archivo: se releen en GitHub" in flat


def test_handoff_uses_v3_as_final_identity_without_storing_its_sha() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    flat = normalized(HANDOFF_PATH)

    assert TAG_V3 in text
    assert V3_RELEASE_TITLE in text
    assert "Anotado, nunca ligero" in text
    assert "| Draft | `false` |" in text
    assert "| Prerelease | `false` |" in text
    assert (
        "Se obtiene únicamente del head remoto vivo de `main` después del "
        "merge del PR documental de issue #438"
    ) in flat
    assert "El commit final **no se almacena anticipadamente**" in flat
    assert set(re.findall(r"\b[0-9a-f]{40}\b", text)) == HISTORICAL_SHAS
    for line in text.splitlines():
        if "v3" in line:
            assert not re.search(r"\b[0-9a-f]{40}\b", line)


def test_handoff_orders_docs_validation_merge_sha_tag_release() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    flat = normalized(HANDOFF_PATH)

    assert (
        "`documentación → validación → merge → SHA post-merge → tag → "
        "Release`"
    ) in flat
    step_positions = [
        text.index(step_marker)
        for step_marker in (
            "1. **Documentación**",
            "2. **Validación**",
            "3. **Merge**",
            "4. **SHA post-merge**",
            "5. **Tag**",
            "6. **Release**",
        )
    ]
    assert step_positions == sorted(step_positions)
    assert "se lee el head remoto de `main` directamente" in flat
    assert (
        "sin commits posteriores no revisados. Ese head validado es el único "
        "origen del commit de `v3`."
    ) in flat
    assert (
        "El tag anotado y el Release quedan asociados exactamente al mismo "
        "commit post-merge."
    ) in flat
    assert (
        "Crear `v3` antes del merge documental volvería a fijar un baseline "
        "incompleto y está prohibido."
    ) in flat


def test_handoff_requires_prior_absence_and_clean_worktree() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    flat = normalized(HANDOFF_PATH)

    assert "'refs/tags/project-os-internal-handoff-v3^{}'" in text
    assert f"gh release view {TAG_V3}" in text
    assert "no debe existir local ni remotamente" in flat
    assert "el Release v3 no debe existir" in flat
    assert "el worktree debe estar limpio" in flat


def test_handoff_local_preflight_is_executable_and_fail_closed() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    # Join `# `-prefixed comment continuation lines so the expected-result
    # annotations inside the command blocks can be matched as full phrases.
    flat = " ".join(text.replace("\n# ", " ").split())

    # The v3 preflight must be executable read-only commands with expected
    # results, not prose-only claims.
    local_tag_absence = text.index(f"git tag --list {TAG_V3}")
    clean_worktree = text.index("git status --short --branch")
    head_matches_approved_sha = text.index("git rev-parse HEAD")
    assert (
        [local_tag_absence, clean_worktree, head_matches_approved_sha]
        == sorted([local_tag_absence, clean_worktree, head_matches_approved_sha])
    )
    assert (
        "salida vacía. El tag v3 no debe existir en el clone local."
    ) in flat
    assert (
        "únicamente la línea de rama (`## ...`), sin entradas de archivos"
    ) in flat
    assert (
        "sin cambios staged, unstaged ni untracked"
    ) in flat
    assert (
        "exactamente el SHA post-merge aprobado, leído en vivo del head "
        "remoto de `main`"
    ) in flat
    for fail_closed_marker in (
        "Cualquier salida no vacía es drift y la operación falla cerrada",
        "Cualquier entrada adicional falla cerrada.",
        "diferencia entre el checkout local y ese SHA falla cerrada",
        "si el worktree no está limpio",
        "si `git rev-parse HEAD` no coincide con el SHA post-merge aprobado",
    ):
        assert fail_closed_marker in flat
    assert (
        "read-only, no crean, actualizan ni eliminan refs"
    ) in flat
    assert (
        "el checkout local debe apuntar exactamente al SHA post-merge "
        "aprobado"
    ) in flat


def test_handoff_separates_exact_pm_approvals_for_tag_and_release() -> None:
    flat = normalized(HANDOFF_PATH)

    assert (
        "Crear y pushear el tag anotado `v3` requiere su propia aprobación "
        "PM exacta"
    ) in flat
    assert (
        "Crear el GitHub Release interno requiere otra aprobación PM exacta "
        "y separada"
    ) in flat
    assert (
        "La aprobación del merge del PR documental no autoriza el tag ni el "
        "Release."
    ) in flat
    assert "Ninguna de esas aprobaciones queda implícita" in flat


def test_handoff_contains_no_tag_or_release_mutation_commands() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for forbidden_mutation in (
        "git fetch",
        "git tag -a",
        "git tag -f",
        "git tag -d",
        "git push origin refs/tags/",
        "git push --delete",
        "git push --force",
        "--force",
        "gh release create",
        "gh release edit",
        "gh release delete",
        "gh release upload",
        "gh release delete-asset",
    ):
        assert forbidden_mutation not in text
    for required_verification in (
        "git ls-remote --exit-code --tags origin",
        "'refs/tags/project-os-internal-handoff-v1^{}'",
        "'refs/tags/project-os-internal-handoff-v2^{}'",
        "'refs/tags/project-os-internal-handoff-v3^{}'",
        "git ls-remote --exit-code --heads origin refs/heads/main",
        f"gh release view {TAG_V1}",
        f"gh release view {TAG_V2}",
        f"gh release view {TAG_V3}",
        "gh repo view codefusion-repo/project-os-v2",
        f"git tag --list {TAG_V3}",
        "git status --short --branch",
        "git rev-parse HEAD",
    ):
        assert required_verification in text
    assert "No requiere tag local" in text
    assert "no dependen de" in text and "remote-tracking" in text


def test_handoff_protects_history_and_limits_authority() -> None:
    flat = normalized(HANDOFF_PATH)

    assert (
        "no se mueven, reutilizan, reemplazan, editan ni eliminan"
    ) in flat
    assert (
        "`v3` tampoco se mueve, reutiliza ni elimina"
    ) in flat
    assert "No habrá `v4` ni otro follow-up de finalización" in flat
    assert "Este documento no autoriza ninguna acción." in flat
    assert (
        "El tag y el Release no autorizan ninguna acción posterior"
    ) in flat
    for separate_gate in (
        "Cierre de issue #438",
        "Cierre de roadmap #274",
        "Archivo del repositorio o cambio de visibilidad o settings",
        "Creación de `agent-os-cli`",
        "transición de contenido",
        "sincronización o backports",
    ):
        assert separate_gate in flat
    assert (
        "No contiene comandos mutantes como autoridad durable"
    ) in flat


def test_handoff_relative_targets_and_adr_anchors_exist() -> None:
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")
    adr = ADR_PATH.read_text(encoding="utf-8")

    relative_targets = (
        "../decisions/0005-public-repository-strategy.md",
        "../security/PUBLIC_READINESS_REVIEW.md",
        "../decisions/0004-public-presentation-and-packaging.md",
    )
    for relative_target in relative_targets:
        assert relative_target in handoff
        assert (HANDOFF_PATH.parent / relative_target).resolve().is_file()
    for heading, anchor in (
        (
            AMENDMENT_1_HEADING,
            "#amendment-1--bounded-internal-handoff-tag-exception-issue-424",
        ),
        (
            AMENDMENT_2_HEADING,
            "#amendment-2--exact-internal-github-release-for-the-fixed-"
            "handoff-baseline-issue-424",
        ),
        (AMENDMENT_3_HEADING, AMENDMENT_3_ANCHOR),
    ):
        assert heading in adr
        assert anchor in handoff
    assert AMENDMENT_3_ANCHOR in adr
