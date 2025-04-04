"""
Unit tests for the utility functions in utils.py.

These tests validate the behavior of:
- `run_command`
- `execute_steps_from_json`
- `replace_with_dict`
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from utils import run_command, execute_steps_from_json, replace_with_dict

def test_replace_with_dict():
    """
    Test the replace_with_dict function to ensure placeholders are replaced correctly.
    """
    input_string = "Hello, {{name}}!"
    replacements = {"name": "World"}
    result = replace_with_dict(input_string, replacements)
    assert result == "Hello, World"

    input_list = ["{{greeting}}, {{name}}!"]
    replacements = {"greeting": "Hi", "name": "Alice"}
    result = replace_with_dict(input_list, replacements)
    assert result == ["Hi, Alice!"]

    with pytest.raises(TypeError):
        replace_with_dict(123, replacements)  # Invalid input type

@patch("subprocess.run")
def test_run_command(mock_subprocess_run):
    """
    Test the run_command function to ensure commands are executed correctly.
    """
    mock_subprocess_run.return_value = MagicMock(stdout="Command executed successfully")
    run_command("echo 'Hello, World!'", use_shell=True)
    mock_subprocess_run.assert_called_once()

    with pytest.raises(FileNotFoundError):
        run_command("nonexistent_command", ignore_errors=False)

def test_execute_steps_from_json():
    """
    Test the execute_steps_from_json function to ensure steps are executed correctly.
    """
    mock_json = """
    {
        "test_section": {
            "defaults": {
                "directory": "/tmp"
            },
            "steps": [
                {
                    "description": "Test command",
                    "command": "echo 'Hello, World!'",
                    "use_shell": true
                }
            ]
        }
    }
    """
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("utils.run_command") as mock_run_command:
            execute_steps_from_json("mock_file.json", "test_section")
            mock_run_command.assert_called_once_with(
                "echo 'Hello, World!'", use_shell=True, timeout=None, ignore_errors=False, directory="/tmp"
            )

    with pytest.raises(ValueError):
        execute_steps_from_json("mock_file.json", "nonexistent_section")