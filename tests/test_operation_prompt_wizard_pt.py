import pytest
from pathlib import Path
import sys

from tools.operation_prompt_wizard import HAVE_PROMPT_TOOLKIT

if not HAVE_PROMPT_TOOLKIT:
    pytest.skip("prompt_toolkit not installed, skipping enhanced interaction tests", allow_module_level=True)

from tools.operation_prompt_wizard import run_wizard_pt, DEFAULT_OPERATIONS_DIR

def setup_mock_operations(tmp_path: Path):
    ops_dir = tmp_path / "operations"
    ops_dir.mkdir()
    (ops_dir / "01-test-op.md").write_text("# Test Operation\n\nINPUT:\n  TARGET_REPOSITORY=<owner/repo>\n\ncontent here")
    return ops_dir

def test_run_wizard_pt_full_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"
    
    inputs = [
        "01", # select operation
        "codefusion-repo/project-os-v2", # variable TARGET_REPOSITORY
        "write" # write preview action
    ]
    
    def mock_prompt(*args, **kwargs):
        if not inputs:
            raise EOFError
        return inputs.pop(0)
        
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt)
    
    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    assert result.exists()
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in result.read_text()

def test_run_wizard_pt_cancel_selection(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"
    
    inputs = ["cancel"]
    
    def mock_prompt(*args, **kwargs):
        return inputs.pop(0)
        
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt)
    
    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is None

def test_run_wizard_pt_cancel_variable_entry(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"
    
    inputs = [
        "01", # select operation
        "cancel", # variable TARGET_REPOSITORY
    ]
    
    def mock_prompt(*args, **kwargs):
        return inputs.pop(0)
        
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt)
    
    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is None

def test_run_wizard_pt_edit_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"
    
    inputs = [
        "01", # select operation
        "codefusion-repo/project-os-v2", # variable TARGET_REPOSITORY
        "edit", # choose edit
        "codefusion-repo/other-repo", # edit TARGET_REPOSITORY
        "write" # choose write
    ]
    
    def mock_prompt(*args, **kwargs):
        return inputs.pop(0)
        
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt)
    
    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    assert "TARGET_REPOSITORY=codefusion-repo/other-repo" in result.read_text()

def test_run_wizard_pt_back_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    (ops_dir / "02-test-op.md").write_text("# Second Operation\n\nINPUT:\n  OTHER_VAR=<foo>\n\ncontent here")
    out_dir = tmp_path / "out"
    
    inputs = [
        "01", # select operation
        "back", # variable TARGET_REPOSITORY -> returns 'operation'
        "02", # select second operation
        "myval", # variable OTHER_VAR
        "write" # choose write
    ]
    
    def mock_prompt(*args, **kwargs):
        return inputs.pop(0)
        
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt)
    
    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    text = result.read_text()
    assert "OTHER_VAR=myval" in text
    assert "Second Operation" in text

