# Coding Setup Tool

This project is a command line tool designed to quickly launch a coding setup, including a VS Code session and a Jupyter Lab environment, using a specified conda environment. 

## Features

- Open a VS Code session in a specified directory.
- Launch Jupyter Lab in the same directory.
- Use a specified conda environment or default to the base environment.
- Easily configurable settings for directory and conda environment.

## Installation

To install the tool, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd coding-setup-tool
pip install -r requirements.txt
```

## Usage

You can run the tool from the command line. The basic syntax is:

```bash
python src/main.py [options]
```

### Options

- `--dir <directory>`: Specify the directory to open in VS Code and Jupyter Lab. Defaults to the current directory.
- `--env <environment>`: Specify the conda environment to use. Defaults to the base environment.

### Example

To launch the tool in the current directory using the base conda environment:

```bash
python src/main.py
```

To specify a different directory and conda environment:

```bash
python src/main.py --dir /path/to/your/project --env myenv
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.