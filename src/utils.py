import json
import shlex
import subprocess

def run_command(command, use_shell=False, timeout=None, ignore_errors=False):
    try:
        # Run the command
        if use_shell:
            # If use_shell is True, the command must be a string
            safe_command = shlex.quote(command)
            result = subprocess.run(
                safe_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=True  # Raise an exception for non-zero exit codes
            )
        else:
            # If use_shell is False, the command must be a list
            result = subprocess.run(
                command,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=True
            )
        # Print the command's output if successful
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

def execute_steps_from_json(json_file, section):
    try:
        # Load the JSON file
        with open(json_file, "r") as file:
            data = json.load(file)

        # Get the selected section
        steps = data.get(section)
        if not steps:
            raise ValueError(f"Section '{section}' not found in the JSON file.")

        # Iterate through the steps in the selected section
        for step in steps:
            description = step.get("description", "No description provided")
            command = step.get("command")
            use_shell = step.get("use_shell", False)
            timeout = step.get("timeout")
            ignore_errors = step.get("ignore_errors", False)

            print(f"Step: {description}")
            print(f"Running command: {command}")

            # Run the command
            run_command(command, use_shell=use_shell, timeout=timeout, ignore_errors=ignore_errors)
            print(f"Step completed: {description}\n")
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{json_file}'.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while executing steps: {str(e)}")


if __name__ == "__main__":
    execute_steps_from_json("commands.json")