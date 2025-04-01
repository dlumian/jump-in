# Jump-In
## A Command Execution Utility

This utility provides a flexible way to execute commands defined in a JSON configuration file. It supports running commands in different environments (e.g., `test`, `prod`) and allows for customization of working directories, error handling, and shell usage.


--- 
## Sections
- [Features](#features)
- [Project Structure](#project-structure)
- [JSON Congifuration](#json-configuration)
- [Usage](#usage)
- [Notes and Caveats](#notes-and-caveats)
- [License](#license)
---

## **Features**
[Back to Top](#sections)

- Execute commands defined in a JSON file (`commands.json`).
- Support for multiple sections (e.g., `test`, `prod`) to organize commands for different use cases.
- Ability to specify working directories for individual commands or use a default directory.
- Optional use of `shell=True` for commands requiring shell features (e.g., `&&` chaining and new sessions).
- Graceful error handling with options to ignore errors or stop execution on failure.

---

## **Project Structure**
[Back to Top](#sections)

```
├── commands.json # JSON file defining commands and their configurations 
├── main.py # Main script to execute commands from the JSON file 
├── README.md # Project documentation
```
---

## **JSON Configuration**
[Back to Top](#sections)

The `commands.json` file defines the commands to be executed. It includes:
- **`meta` Section:** Global settings, such as the default working directory.
- **Sections (e.g., `test`, `prod`):** Organized lists of commands for different environments.

### Example `commands.json`:
```json
{
  "meta": {
    "default_directory": "."
  },
  "test": [
    {
      "description": "Run unit tests",
      "command": ["pytest", "tests/"],
      "use_shell": false,
      "ignore_errors": false,
      "directory": "./tests"
    },
    {
      "description": "Check code formatting",
      "command": ["black", "--check", "."],
      "use_shell": false,
      "ignore_errors": true
    }
  ],
  "prod": [
    {
      "description": "Activate Conda environment and start Jupyter Lab",
      "command": "conda activate myenv && jupyter lab",
      "use_shell": true,
      "ignore_errors": false
    },
    {
      "description": "Deploy application",
      "command": ["deploy_tool", "--env", "prod"],
      "use_shell": false,
      "ignore_errors": false,
      "directory": "./deployment"
    }
  ]
}
```
### Usage
[Back to Top](#sections)

**Command-Line Execution**
Run the utility from the command line using the main.py script. Specify the JSON file and the section to execute.

**Arguments**
json_file: Path to the JSON configuration file (e.g., commands.json).
section: The section of the JSON file to execute (e.g., test, prod).


### Notes and Caveats
[Back to Top](#sections)
#### Subprocess Shell=True
Using `shell=True` can introduce shell injection vulnerabilities if user input is included in the command.
`shell=True` is used here when necessary, such as for commands requiring shell features like &&, pipes (|), or redirection (>).
Example: "conda activate myenv && jupyter lab".
Basic sanitization is used, but caution is advised for monitoring using input.

#### Notebook Use
Running this utility from a Jupyter Notebook is not recommended due to limitations with terminal-specific commands and interactive processes. Issues may include:
- Commands like `conda activate` or `jupyter lab` behaving unexpectedly.
- Long-running or GUI-based processes can hang the notebook kernel.
- The working directory in a notebook may differ from the script's expected behavior.

## License
[Back to Top](#sections)

This project is licensed under the MIT License. See the LICENSE file for details.

