import os
import json
import shlex
import subprocess

def run_command(command, use_shell=False, timeout=None, ignore_errors=False, directory=None):
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
        default_directory = setup_details.get("default_directory", ".")
        if not default_directory:
            default_directory = os.getcwd()

        # Iterate through the steps in the selected section
        for cnt, step in enumerate(steps):
            description = step.get("description", "No description provided")
            command = step.get("command")
            use_shell = step.get("use_shell", False)
            timeout = step.get("timeout")
            ignore_errors = step.get("ignore_errors", False)
            directory = step.get("directory", default_directory)

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

if __name__ == "__main__":
    json_path = './../configs/commands.json'
    section_key = 'basic_tests'
    execute_steps_from_json(json_path, section_key)