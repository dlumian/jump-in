import argparse
from utils import execute_steps_from_json

def main():
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