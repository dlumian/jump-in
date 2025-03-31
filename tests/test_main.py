import unittest
from unittest.mock import patch, MagicMock
import sys
import os

class TestMain(unittest.TestCase):

    @patch('src.main.launch_vscode')
    @patch('src.main.launch_jupyter')
    @patch('src.main.activate_conda_env')
    def test_launch_setup(self, mock_activate, mock_launch_jupyter, mock_launch_vscode):
        # Simulate command line arguments
        sys.argv = ['main.py', '--directory', '/path/to/project', '--env', 'myenv']
        
        # Import the main module after setting sys.argv
        import src.main
        
        # Check if the conda environment activation was called
        mock_activate.assert_called_once_with('myenv')
        
        # Check if VS Code and Jupyter Lab were launched
        mock_launch_vscode.assert_called_once_with('/path/to/project')
        mock_launch_jupyter.assert_called_once_with('/path/to/project')

    @patch('src.main.launch_vscode')
    @patch('src.main.launch_jupyter')
    @patch('src.main.activate_conda_env')
    def test_default_setup(self, mock_activate, mock_launch_jupyter, mock_launch_vscode):
        # Simulate command line arguments with defaults
        sys.argv = ['main.py']
        
        # Import the main module after setting sys.argv
        import src.main
        
        # Check if the default conda environment activation was called
        mock_activate.assert_called_once_with('base')
        
        # Check if VS Code and Jupyter Lab were launched in the current directory
        current_directory = os.getcwd()
        mock_launch_vscode.assert_called_once_with(current_directory)
        mock_launch_jupyter.assert_called_once_with(current_directory)

if __name__ == '__main__':
    unittest.main()