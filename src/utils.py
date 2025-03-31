import json
import subprocess

def run_command(command, timeout=None):
    try:
        # Run the command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,  # Raise an exception for non-zero exit codes
            timeout=timeout  # Optional timeout
        )
        # Return the command's output if successful
        return result.stdout
    except FileNotFoundError:
        print(f"Error: Command not found: {command[0]}")
    except PermissionError:
        print(f"Permission denied: Unable to execute {command[0]}")
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {e.timeout} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error message: {e.stderr.strip()}")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def execute_steps_from_json(json_file):
    try:
        # Load the JSON file
        with open(json_file, "r") as file:
            data = json.load(file)
        
        # Iterate through the steps
        for step in data.get("steps", []):
            description = step.get("description", "No description provided")
            command = step.get("command")
            timeout = step.get("timeout")
            ignore_errors = step.get("ignore_errors", False)
            
            print(f"Step: {description}")
            print(f"Running command: {' '.join(command)}")
            
            # Run the command
            run_command(command, timeout=timeout, ignore_errors=ignore_errors)
            print(f"Step completed: {description}\n")
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{json_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred while executing steps: {str(e)}")

if __name__ == "__main__":
    execute_steps_from_json("setup_steps.json")