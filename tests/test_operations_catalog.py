import os
import re

PM_QUESTION_ALLOWED = {"00", "05", "30", "31", "32"}
PM_FEEDBACK_OPTIONAL_ALLOWED = {"30", "31", "32"}
PM_FEEDBACK_REQUIRED_ALLOWED = {"08"}


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

    assert len(templates) == 33

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

        assert "PM_QUESTION" not in req_vars, f"PM_QUESTION must never be required in {template}"
        if "PM_QUESTION" in opt_vars:
            assert idx in PM_QUESTION_ALLOWED, f"PM_QUESTION not justified in {template}"
        if "PM_FEEDBACK_HUMANO" in req_vars:
            assert idx in PM_FEEDBACK_REQUIRED_ALLOWED, f"PM_FEEDBACK_HUMANO required only for correction routing: {template}"
        if "PM_FEEDBACK_HUMANO" in opt_vars:
            assert idx in PM_FEEDBACK_OPTIONAL_ALLOWED, f"PM_FEEDBACK_HUMANO not justified in {template}"
        expected_discursive = [
            var for var in [*req_vars, *opt_vars] if var in {"PM_QUESTION", "PM_FEEDBACK_HUMANO"}
        ]
        assert expected["discursive"] == expected_discursive, (
            f"Discursive vars mismatch in docs row {idx}: {expected['discursive']} vs {expected_discursive}"
        )

        # Check RECOMMENDED_NEXT_OPERATION
        next_op_match = re.search(r'RECOMMENDED_NEXT_OPERATION:\n(.*?)(?:\n\n|\Z)', content, re.DOTALL)
        assert next_op_match, f"No RECOMMENDED_NEXT_OPERATION in {template}"

        # Check no live-state durable content
        assert "github.com/" not in content, f"Live state found in {template}"

def test_no_unjustified_kernel_growth():
    # Enforce no kernel changes by checking git status of kernel/
    import subprocess
    result = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD", "kernel/"], capture_output=True, text=True)
    changed_files = [f for f in result.stdout.strip().split('\n') if f]
    assert not changed_files, f"Kernel files were modified: {changed_files}"
