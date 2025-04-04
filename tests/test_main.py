"""
Unit tests for the main.py script.

These tests validate the behavior of the main function and its integration with utils.py.
"""
import os
print(os.cwd())

from datascifuncs.tools import check_directory_name
target_name = "jump-in"
check_directory_name(target_name=target_name)
print(os.cwd())
import pytest
from unittest.mock import patch
from main import main

@patch("argparse.ArgumentParser.parse_args")
@patch("utils.execute_steps_from_json")
def test_main(mock_execute_steps_from_json, mock_parse_args):
    """
    Test the main function to ensure it parses arguments and calls execute_steps_from_json.
    """
    mock_parse_args.return_value = argparse.Namespace(
        json_file="mock_file.json", section_key="test_section"
    )
    main()
    mock_execute_steps_from_json.assert_called_once_with("mock_file.json", "test_section")