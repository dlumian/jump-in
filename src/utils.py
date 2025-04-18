"""
Utility functions for the Jump-In project.

This module provides functions to:
- Execute shell commands.
- Parse and execute steps from a JSON configuration file.
- Replace placeholders in strings using a dictionary.
"""

import os
import json
import shlex
import subprocess

def run_command(command, use_shell=False, timeout=None, ignore_errors=False, directory=None):
    """
    Execute a shell command with optional parameters.

    Args:
        command (str): The command to execute.
        use_shell (bool): Whether to execute the command in a shell environment. Default is False.
        timeout (int, optional): Timeout in seconds for the command. Default is None.
        ignore_errors (bool): Whether to ignore errors during execution. Default is False.
        directory (str, optional): The directory in which to execute the command. Default is the current working directory.

    Raises:
        FileNotFoundError: If the command is not found.
        subprocess.TimeoutExpired: If the command times out.
        subprocess.CalledProcessError: If the command fails and `ignore_errors` is False.
        Exception: For any other unexpected errors.

    Returns:
        None
    """
    try:
        # Use the specified directory or default to the current working directory
        cwd = directory or os.getcwd()
        # Run the command
        if use_shell:
            safe_command = shlex.quote(command)
            result = subprocess.run(
                safe_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=True,
                cwd=cwd  # Set the working directory
            )
        else:
            result = subprocess.run(
                command,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=True,
                cwd=cwd  # Set the working directory
            )
        print(result.stdout)
    except FileNotFoundError:
        print(f"Error: Command not found: {command}")
        if not ignore_errors:
            raise
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {e.timeout} seconds")
        if not ignore_errors:
            raise
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error message: {e.stderr.strip()}")
        if not ignore_errors:
            raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        if not ignore_errors:
            raise

def execute_steps_from_json(json_file, section_key):
    """
    Execute steps defined in a JSON configuration file.

    Args:
        json_file (str): Path to the JSON configuration file.
        section_key (str): The key of the section in the JSON file to execute.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        json.JSONDecodeError: If the JSON file cannot be parsed.
        ValueError: If the specified section or steps are not found in the JSON file.
        Exception: For any other unexpected errors.

    Returns:
        None
    """
    try:
        print(f"Jumping into: {json_file}.")
        print(f"Running setup for: {section_key}.\n")

        # Load the JSON file
        with open(json_file, "r") as f:
            data = json.load(f)

        setup_details = data.get(section_key)
        if not setup_details:
            raise ValueError(f"Section '{section_key}' not found in the JSON file.")

        steps = setup_details.get("steps")
        if not steps:
            raise ValueError(f"Steps not defined in '{section_key}'.")

        # Get the default directory
        defaults = setup_details.get("defaults", {})
        default_directory = defaults.get('directory')
        if not default_directory:
            defaults['directory'] = os.getcwd()

        # Iterate through the steps in the selected section
        for cnt, step in enumerate(steps):
            step_settings = defaults.copy()

            description = step.get("description", "No description provided")
            command = step.get("command")
            use_shell = step.get("use_shell", False)
            timeout = step.get("timeout")
            ignore_errors = step.get("ignore_errors", False)
            directory = step.get("directory")
            if not directory:
                directory = step_settings['directory']
            # String replacement for command
            command = replace_with_dict(command, step_settings, open_symbol="{{")

            print(f"Step {cnt}: {description}")
            print(f"Running command: {command} in directory: {directory}")

            # Run the command
            run_command(command, use_shell=use_shell, timeout=timeout, ignore_errors=ignore_errors, directory=directory)
            print(f"Step {cnt} completed: {description}\n")
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{json_file}'.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while executing steps: {str(e)}")

def replace_with_dict(input_data, replacements, open_symbol="{{", close_symbol="}}"):
    """
    Replace placeholders in a string or list of strings using a dictionary.

    Args:
        input_data (str | list): The input string or list of strings.
        replacements (dict): A dictionary where keys are placeholders (without symbols)
                             and values are the replacements.
        open_symbol (str): The opening symbol for placeholders. Default is "{{".
        close_symbol (str): The closing symbol for placeholders. Default is "}}".

    Raises:
        TypeError: If the input data is not a string or list of strings.

    Returns:
        str | list: The input data with placeholders replaced by their corresponding values.
    """
    # Perform the replacement
    def replace_in_string(s):
        for key, value in replacements.items():
            placeholder = f"{open_symbol}{key}{close_symbol}"
            s = s.replace(placeholder, value)
        return s

    # Handle both strings and lists of strings
    if isinstance(input_data, str):
        return replace_in_string(input_data)
    elif isinstance(input_data, list):
        return [replace_in_string(item) for item in input_data]
    else:
        raise TypeError("Input data must be a string or a list of strings.")

if __name__ == "__main__":
    json_path = './../configs/commands.json'
    section_key = 'basic_tests'
    execute_steps_from_json(json_file=json_path, section_key=section_key)