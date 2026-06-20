"""Tests for the read-only GitHub traceability auditor."""

from __future__ import annotations

import json
import subprocess
import textwrap

import pytest

from tools.audit_traceability import (
    AuditError,
    ChangedFile,
    CLOSURE_SECTION_LABELS,
    Comment,
    Finding,
    GithubClient,
    Issue,
    PullRequest,
    _issue_from_payload,
    analyze_issue,
    analyze_pull_request,
    main,
)

REPO = "acme/widgets"


def codes(findings: list[Finding]) -> set[str]:
    return {finding.code for finding in findings}


def comments(*items: Comment) -> tuple[Comment, ...]:
    return tuple(items)


def comment(
    body: str,
    *,
    id: int = 1,
    author: str = "agent",
    created_at: str = "2026-06-01T10:00:00Z",
) -> Comment:
    return Comment(id=id, author_login=author, body=body, created_at=created_at)


def closed_issue(*issue_comments: Comment) -> Issue:
    return Issue(
        number=10,
        title="Done work",
        body="## Scope\n- `src/widgets/`\n",
        state="closed",
        closed_at="2026-06-01T12:00:00Z",
        comments=comments(*issue_comments),
    )


def packet_text(
    *,
    validation: str = "- `python3 -m pytest tests/ -q`\n- Result: PASS",
    exceptions: str = "None",
    omit: str | None = None,
    spanish: bool = False,
) -> str:
    labels = {
        "completion_evidence": "Completion evidence",
        "validation_evidence": "Validation evidence",
        "accepted_exceptions": "Accepted exceptions",
        "boundaries_preserved": "Boundaries preserved",
        "friction_note": "Friction note",
        "references": "References",
    }
    if spanish:
        labels.update(
            {
                "completion_evidence": "Evidencia de finalización",
                "validation_evidence": "Evidencia de validación",
                "accepted_exceptions": "Excepciones aceptadas",
                "boundaries_preserved": "Límites preservados",
                "friction_note": "Nota de fricción",
                "references": "Referencias",
            }
        )
    bodies = {
        "completion_evidence": "- Implemented the scoped change.",
        "validation_evidence": validation,
        "accepted_exceptions": exceptions,
        "boundaries_preserved": "- No labels, merge, or closure automation.",
        "friction_note": "- None.",
        "references": "- PR #20.",
    }
    parts: list[str] = []
    for key in labels:
        if key == omit:
            continue
        parts.append(f"## {labels[key]}\n\n{bodies[key]}")
    return "\n\n".join(parts)


def issue_body(scope: str, out_of_scope: str = "None") -> str:
    return textwrap.dedent(
        f"""\
        ## Objective

        Implement the requested change.

        ## Scope

        {scope}

        ## Out of scope

        {out_of_scope}
        """
    )


def pr(
    body: str,
    *,
    files: tuple[ChangedFile, ...] = (),
    title: str = "Implement widget",
    comments_: tuple[Comment, ...] = (),
) -> PullRequest:
    return PullRequest(number=20, title=title, body=body, state="open", comments=comments_, changed_files=files)


def test_closed_issue_with_no_comments_reports_missing_closure_packet() -> None:
    found = codes(analyze_issue(REPO, closed_issue()))

    assert found == {"TRACE-CLOSURE-PACKET-MISSING"}


def test_closed_issue_with_comments_but_no_closure_packet_reports_missing_closure_packet() -> None:
    found = codes(analyze_issue(REPO, closed_issue(comment("Looks good.", id=1))))

    assert "TRACE-CLOSURE-PACKET-MISSING" in found


@pytest.mark.parametrize("missing", tuple(CLOSURE_SECTION_LABELS))
def test_each_missing_required_closure_section_is_reported(missing: str) -> None:
    findings = analyze_issue(REPO, closed_issue(comment(packet_text(omit=missing), id=2)))

    missing_findings = [finding for finding in findings if finding.code == "TRACE-CLOSURE-SECTION-MISSING"]
    assert any(CLOSURE_SECTION_LABELS[missing] in finding.message for finding in missing_findings)


def test_spanish_closure_section_aliases_are_recognized() -> None:
    findings = analyze_issue(REPO, closed_issue(comment(packet_text(spanish=True), id=2)))

    assert codes(findings) == set()


def test_validation_command_without_result_is_reported() -> None:
    body = packet_text(validation="- `python3 -m pytest tests/ -q`")

    found = codes(analyze_issue(REPO, closed_issue(comment(body, id=2))))

    assert "TRACE-VALIDATION-RESULT-MISSING" in found


def test_skipped_validation_with_reason_is_accepted() -> None:
    body = packet_text(validation="- `python3 -m pytest tests/ -q` not run because dependencies are unavailable.")

    found = codes(analyze_issue(REPO, closed_issue(comment(body, id=2))))

    assert "TRACE-VALIDATION-RESULT-MISSING" not in found


def test_exception_with_matching_pm_decision_is_accepted() -> None:
    body = packet_text(exceptions="- Accepted CI skip exception.")
    issue = closed_issue(comment(body, id=2, author="pm"))

    found = codes(analyze_issue(REPO, issue, pm_login="pm"))

    assert "TRACE-EXCEPTION-PM-DECISION-MISSING" not in found


def test_exception_without_pm_decision_is_reported() -> None:
    body = packet_text(exceptions="- Accepted CI skip exception.")
    issue = closed_issue(comment(body, id=2, author="agent"))

    found = codes(analyze_issue(REPO, issue, pm_login="pm"))

    assert "TRACE-EXCEPTION-PM-DECISION-MISSING" in found


def test_non_empty_exception_without_pm_login_is_reported() -> None:
    body = packet_text(exceptions="- Accepted CI skip exception.")
    issue = closed_issue(comment(body, id=2, author="agent"))

    found = codes(analyze_issue(REPO, issue))

    assert "TRACE-PM-LOGIN-MISSING" in found


def test_late_closure_packet_is_reported_as_timing_warning() -> None:
    issue = closed_issue(comment(packet_text(), id=2, created_at="2026-06-01T12:01:00Z"))

    found = codes(analyze_issue(REPO, issue))

    assert "TRACE-CLOSURE-PACKET-LATE" in found


def test_exact_duplicate_comments_are_reported() -> None:
    issue = Issue(
        number=10,
        title="Open",
        body="",
        state="open",
        comments=comments(comment("Same **body**.", id=1), comment("Same body.", id=2)),
    )

    found = codes(analyze_issue(REPO, issue))

    assert "TRACE-DUPLICATE-COMMENT" in found


def test_near_duplicate_comments_are_reported_with_confidence() -> None:
    issue = Issue(
        number=10,
        title="Open",
        body="",
        state="open",
        comments=comments(
            comment("Closure evidence posted with validation passing and boundaries preserved.", id=1),
            comment("Closure evidence posted with validation passed and boundaries preserved.", id=2),
        ),
    )

    findings = analyze_issue(REPO, issue)

    near = [finding for finding in findings if finding.code == "TRACE-NEAR-DUPLICATE-COMMENT"]
    assert near
    assert near[0].confidence == "medium"


def test_single_outcome_pr_is_not_reported() -> None:
    findings = analyze_pull_request(REPO, pr("Closes #10"))

    assert "TRACE-PR-MULTI-OUTCOME" not in codes(findings)


def test_pr_with_multiple_closing_outcomes_is_reported() -> None:
    findings = analyze_pull_request(REPO, pr("Closes #10\nCloses #11"))

    found = [finding for finding in findings if finding.code == "TRACE-PR-MULTI-OUTCOME"]
    assert found
    assert found[0].confidence == "high"


def test_pr_acknowledging_unrelated_work_is_reported() -> None:
    findings = analyze_pull_request(REPO, pr("Closes #10\n\nAlso includes unrelated work from #12."))

    assert "TRACE-PR-MULTI-OUTCOME" in codes(findings)


def test_in_scope_changed_file_set_is_not_reported() -> None:
    issue = Issue(
        number=10,
        title="Widget",
        body=issue_body("- `src/widgets/`\n- `tests/widgets/`"),
        state="open",
    )
    pull = pr(
        "Closes #10",
        files=(ChangedFile("src/widgets/app.py"), ChangedFile("tests/widgets/test_app.py")),
    )

    assert "TRACE-PR-OUT-OF-SCOPE-FILE" not in codes(analyze_pull_request(REPO, pull, [issue]))


def test_high_confidence_out_of_scope_changed_file_is_reported() -> None:
    issue = Issue(
        number=10,
        title="Widget",
        body=issue_body("- `src/widgets/`", "- `docs/`"),
        state="open",
    )
    pull = pr("Closes #10", files=(ChangedFile("docs/traceability.md"),))

    findings = analyze_pull_request(REPO, pull, [issue])

    scoped = [finding for finding in findings if finding.code == "TRACE-PR-OUT-OF-SCOPE-FILE"]
    assert scoped
    assert scoped[0].confidence == "high"


def test_scope_without_machine_checkable_boundary_reports_limited_confidence() -> None:
    issue = Issue(number=10, title="Widget", body=issue_body("Improve CI reliability."), state="open")
    pull = pr("Closes #10", files=(ChangedFile(".github/workflows/validate.yml"),))

    findings = analyze_pull_request(REPO, pull, [issue])

    scoped = [finding for finding in findings if finding.code == "TRACE-PR-OUT-OF-SCOPE-FILE"]
    assert scoped
    assert scoped[0].confidence == "low"


class FakeClient:
    issue = Issue(number=10, title="Open", body="", state="open")
    pr_item = PullRequest(number=20, title="PR", body="Closes #10", state="open")
    range_result = ([], [])

    def __init__(self, repository: str) -> None:
        self.repository = repository

    def ensure_ready(self) -> None:
        return None

    def fetch_issue(self, number: int) -> Issue:
        return self.issue

    def fetch_pull_request(self, number: int) -> PullRequest:
        return self.pr_item

    def search_range(self, since: str, until: str, kind: str, limit: int) -> tuple[list[int], list[int]]:
        return self.range_result


class NoAuthGithubClient(GithubClient):
    def ensure_ready(self) -> None:
        return None


def test_human_and_json_outputs_report_same_findings(capsys: pytest.CaptureFixture[str]) -> None:
    class FindingClient(FakeClient):
        issue = closed_issue()

    human_code = main(["--repository", REPO, "--issue", "10"], client_cls=FindingClient)
    human = capsys.readouterr().out

    json_code = main(["--repository", REPO, "--issue", "10", "--json"], client_cls=FindingClient)
    payload = json.loads(capsys.readouterr().out)

    human_codes = {line.split(" ", 1)[0] for line in human.splitlines() if line.startswith("TRACE-")}
    json_codes = {finding["code"] for finding in payload["findings"]}

    assert human_code == 1
    assert json_code == 1
    assert human_codes == json_codes == {"TRACE-CLOSURE-PACKET-MISSING"}


def test_cli_exit_codes_for_clean_findings_and_tooling_failure(capsys: pytest.CaptureFixture[str]) -> None:
    class FindingClient(FakeClient):
        issue = closed_issue()

    class FailureClient(FakeClient):
        def ensure_ready(self) -> None:
            raise AuditError("gh auth failed")

    assert main(["--repository", REPO, "--issue", "10"], client_cls=FakeClient) == 0
    capsys.readouterr()
    assert main(["--repository", REPO, "--issue", "10"], client_cls=FindingClient) == 1
    capsys.readouterr()
    assert main(["--repository", REPO, "--issue", "10"], client_cls=FailureClient) == 2


def test_cli_accepts_bounded_range_without_live_network(capsys: pytest.CaptureFixture[str]) -> None:
    class RangeClient(FakeClient):
        range_result = ([10], [20])

        def fetch_pull_request(self, number: int) -> PullRequest:
            return PullRequest(number=20, title="PR", body="Closes #10", state="open")

    assert (
        main(
            ["--repository", REPO, "--since", "2026-06-01", "--until", "2026-06-02", "--range-kind", "both"],
            client_cls=RangeClient,
        )
        == 0
    )
    assert "traceability audit: OK" in capsys.readouterr().out


def test_paged_comments_payload_parses_into_comment_objects(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = [
        [
            {
                "id": index,
                "user": {"login": "agent"},
                "body": f"Comment {index}",
                "created_at": "2026-06-01T10:00:00Z",
                "html_url": f"https://example.test/comments/{index}",
            }
            for index in range(1, 101)
        ],
        [
            {
                "id": 101,
                "user": {"login": "pm"},
                "body": "Final comment",
                "created_at": "2026-06-01T10:01:00Z",
                "html_url": "https://example.test/comments/101",
            }
        ],
    ]
    commands: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        commands.append(cmd)
        page_arg = next(part for part in cmd if part.startswith("page="))
        page = int(page_arg.split("=", 1)[1])
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(pages[page - 1]), stderr="")

    monkeypatch.setattr("tools.audit_traceability.subprocess.run", fake_run)

    parsed = GithubClient(REPO)._fetch_issue_comments(10)

    assert len(parsed) == 101
    assert parsed[0] == Comment(
        id=1,
        author_login="agent",
        body="Comment 1",
        created_at="2026-06-01T10:00:00Z",
        url="https://example.test/comments/1",
    )
    assert parsed[-1].author_login == "pm"
    assert all("--jq" not in command and "--method" in command and "GET" in command for command in commands)
    assert [part for command in commands for part in command if part.startswith("page=")] == ["page=1", "page=2"]


def test_paged_pr_files_payload_parses_into_changed_file_objects(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = [
        {"filename": "tools/audit_traceability.py", "status": "modified"},
        {"filename": "tests/test_audit_traceability.py", "status": "added"},
    ]

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        assert "--jq" not in cmd
        assert "--method" in cmd and "GET" in cmd
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(payload), stderr="")

    monkeypatch.setattr("tools.audit_traceability.subprocess.run", fake_run)

    parsed = GithubClient(REPO)._fetch_pr_files(20, {"changed_files": 2})

    assert parsed == (
        ChangedFile("tools/audit_traceability.py", "modified"),
        ChangedFile("tests/test_audit_traceability.py", "added"),
    )


def test_malformed_paged_json_returns_tooling_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        endpoint = cmd[4]
        if endpoint == f"/repos/{REPO}/issues/10":
            payload = {"number": 10, "title": "Issue", "state": "open", "body": ""}
            return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(payload), stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="{not json", stderr="")

    monkeypatch.setattr("tools.audit_traceability.subprocess.run", fake_run)

    assert main(["--repository", REPO, "--issue", "10"], client_cls=NoAuthGithubClient) == 2
    assert "invalid JSON" in capsys.readouterr().err


def test_unsupported_paged_item_shape_returns_tooling_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        endpoint = cmd[4]
        if endpoint == f"/repos/{REPO}/issues/10":
            payload = {"number": 10, "title": "Issue", "state": "open", "body": ""}
            return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(payload), stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps([{"id": 1}, "bad item"]), stderr="")

    monkeypatch.setattr("tools.audit_traceability.subprocess.run", fake_run)

    assert main(["--repository", REPO, "--issue", "10"], client_cls=NoAuthGithubClient) == 2
    assert "unsupported paginated item" in capsys.readouterr().err


def test_read_failure_returns_tooling_error(capsys: pytest.CaptureFixture[str]) -> None:
    class FetchFailureClient(FakeClient):
        def fetch_issue(self, number: int) -> Issue:
            raise AuditError("inaccessible repository")

    assert main(["--repository", REPO, "--issue", "10"], client_cls=FetchFailureClient) == 2
    assert "inaccessible repository" in capsys.readouterr().err


def test_unsupported_payload_fields_are_tooling_errors() -> None:
    with pytest.raises(AuditError):
        _issue_from_payload({"number": 10, "state": "open"}, ())
