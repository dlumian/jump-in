"""
Main entry point for the Jump-In project.

This script uses argparse to allow users to specify a JSON file and a section key
to execute commands defined in the JSON configuration file.
"""

import argparse
from utils import execute_steps_from_json

def main():
    """
    Parse command-line arguments and execute steps from the specified JSON file.

    The script expects two arguments:
    - `json_file`: Path to the JSON configuration file.
    - `section_key`: The key of the section in the JSON file to execute.

    Example usage:
        python main.py path/to/commands.json section_key
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Execute steps from a JSON configuration file.")
    parser.add_argument(
        "json_file",
        type=str,
        help="Path to the JSON configuration file."
    )
    parser.add_argument(
        "section_key",
        type=str,
        help="Key of the section in the JSON file to execute."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Execute the steps from the JSON file
    execute_steps_from_json(json_file=args.json_file, section_key=args.section_key)

if __name__ == "__main__":
    main()    