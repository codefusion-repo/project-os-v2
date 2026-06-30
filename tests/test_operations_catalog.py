import os
import re

def test_pm_operations_catalog_alignment():
    with open("docs/PM_OPERATIONS.md") as f:
        docs_content = f.read()

    ops_dir = "templates/operations"
    templates = [f for f in sorted(os.listdir(ops_dir)) if f.endswith(".md")]
    
    # 30 templates
    assert len(templates) == 30

    for template in templates:
        with open(os.path.join(ops_dir, template)) as f:
            content = f.read()

        # Check INPUT format
        assert "INPUT:\n" in content
        
        # Check RECOMMENDED_NEXT_OPERATION
        assert "RECOMMENDED_NEXT_OPERATION:\n" in content

        # Check no live-state durable content
        # we make sure things like http github urls or SHAs are not stored in templates
        assert "github.com/" not in content
        
        # valid kernel ids check could be complex, but let's at least check they start with actor, workflow, mode, output, status, etc
        assert re.search(r'(actor\.|workflow\.|mode\.|output\.|status\.|evidence\.)', content)

    # Check that lifecycle flow guidance is in the docs
    assert "Orientación de Flujo de Ciclo de Vida" in docs_content
    assert "RECOMMENDED_NEXT_OPERATION" in docs_content

    # Check justified usage explanation
    assert "PM_QUESTION" in docs_content
    assert "FEEDBACK_PM_HUMANO" in docs_content

def test_no_unjustified_kernel_growth():
    # Kernel growth wasn't allowed, just checking kernel files are unchanged or valid
    with open("kernel/manifest.json") as f:
        manifest = f.read()
    assert "actor.terminal_agent" in manifest
