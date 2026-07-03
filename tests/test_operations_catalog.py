import os
import re

HUMAN_CONTEXT_VARIABLES = {"PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"}
LEGACY_PM_QUESTION_PATTERN = re.compile(r"\bPM_QUESTION\b")


def parse_markdown_table(content: str, header: str):
    lines = content.split('\n')
    table_lines = []
    in_table = False
    for line in lines:
        if header in line:
            in_table = True
        elif in_table and line.strip().startswith('|'):
            table_lines.append(line.strip())
        elif in_table and not line.strip():
            if table_lines:
                break
    return table_lines


def split_vars(cell: str) -> list[str]:
    return [v.strip() for v in cell.split(',')] if cell != "(none)" else []


def assert_unique(values: list[str], context: str) -> None:
    assert len(values) == len(set(values)), f"Duplicated variables in {context}: {values}"

def test_pm_operations_catalog_alignment():
    with open("docs/PM_OPERATIONS.md") as f:
        docs_content = f.read()

    # Find the matrix
    matrix_lines = parse_markdown_table(docs_content, "| Template | Req Variables | Opt Variables | Discursive | Recommended Next Operation |")
    # strip separator
    matrix_lines = matrix_lines[1:]

    matrix = {}
    for line in matrix_lines:
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) == 5:
            template_idx = parts[0]
            req_vars = split_vars(parts[1])
            opt_vars = split_vars(parts[2])
            discursive_vars = split_vars(parts[3])
            assert_unique(req_vars, f"docs required row {template_idx}")
            assert_unique(opt_vars, f"docs optional row {template_idx}")
            assert_unique(discursive_vars, f"docs discursive row {template_idx}")
            matrix[template_idx] = {
                "req": req_vars,
                "opt": opt_vars,
                "discursive": discursive_vars,
                "next": parts[4]
            }

    ops_dir = "templates/operations"
    templates = [f for f in sorted(os.listdir(ops_dir)) if f.endswith(".md")]

    assert len(templates) == 38

    for template in templates:
        idx = template[:2]
        with open(os.path.join(ops_dir, template)) as f:
            content = f.read()

        # Parse INPUT block
        input_match = re.search(r'INPUT:\n(.*?)(?:\n\n[A-Z_]+:|\Z)', content, re.DOTALL)
        assert input_match, f"No INPUT block in {template}"
        input_text = input_match.group(1).strip()

        req_vars = []
        opt_vars = []
        if input_text and "(none)" not in input_text:
            for line in input_text.split('\n'):
                line = line.strip()
                if not line: continue
                # Match VAR=<VAR>
                var_match = re.search(r'([A-Z_]+)=', line)
                if var_match:
                    var_name = var_match.group(1)
                    if "# optional" in line:
                        opt_vars.append(var_name)
                    else:
                        req_vars.append(var_name)

        assert_unique(req_vars, template)
        assert_unique(opt_vars, template)
        expected = matrix.get(idx, {"req": [], "opt": [], "discursive": [], "next": ""})
        assert req_vars == expected["req"], f"Req vars mismatch in {template}: {req_vars} vs {expected['req']}"
        assert opt_vars == expected["opt"], f"Opt vars mismatch in {template}: {opt_vars} vs {expected['opt']}"

        assert not LEGACY_PM_QUESTION_PATTERN.search(content), f"legacy PM_QUESTION token remains in {template}"
        assert HUMAN_CONTEXT_VARIABLES.isdisjoint(req_vars), f"human context vars must be optional in {template}"
        assert HUMAN_CONTEXT_VARIABLES.issubset(opt_vars), f"missing optional human context vars in {template}"
        expected_discursive = [
            var for var in [*req_vars, *opt_vars] if var in HUMAN_CONTEXT_VARIABLES
        ]
        assert expected["discursive"] == expected_discursive, (
            f"Discursive vars mismatch in docs row {idx}: {expected['discursive']} vs {expected_discursive}"
        )

        # Check RECOMMENDED_NEXT_OPERATION
        next_op_match = re.search(r'RECOMMENDED_NEXT_OPERATION:\n(.*?)(?:\n\n|\Z)', content, re.DOTALL)
        assert next_op_match, f"No RECOMMENDED_NEXT_OPERATION in {template}"

        # Check no live-state durable content
        assert "github.com/" not in content, f"Live state found in {template}"

def test_issue_343_kernel_growth_is_limited_to_manual_implementation_contracts():
    # Kernel growth is allowed here only for the KOPS.2 manual no-write path,
    # plus kernel files authorized by later PM-approved kernel-growth issues.
    import subprocess
    result = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD", "kernel/"], capture_output=True, text=True)
    changed_files = [f for f in result.stdout.strip().split('\n') if f]
    allowed_files = {
        "kernel/workflows.json",
        "kernel/outputs.json",
        # Authorized by #376 (MOSDLC.6a) per docs/decisions/0001: minimal,
        # internal-only, gated local/staging deploy-execution kernel support.
        # Content-level growth stays pinned by CANONICAL_KERNEL_ENTRY_IDS in
        # tests/test_pm_operation_contracts.py::test_issue_324_kernel_entry_ids_are_unchanged.
        "kernel/actors.json",
        "kernel/evidence.json",
        "kernel/execution_modes.json",
    }
    assert set(changed_files).issubset(allowed_files), f"Unexpected kernel files were modified: {changed_files}"

    if changed_files:
        import json
        from pathlib import Path

        workflows = json.loads(Path("kernel/workflows.json").read_text(encoding="utf-8"))
        outputs = json.loads(Path("kernel/outputs.json").read_text(encoding="utf-8"))
        workflow_ids = {entry["id"] for entry in workflows["entries"]}
        output_ids = {entry["id"] for entry in outputs["entries"]}
        assert "workflow.issue_implementation_manual" in workflow_ids
        assert "output.manual_implementation_plan" in output_ids
