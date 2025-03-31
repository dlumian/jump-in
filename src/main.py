import argparse
import os
import subprocess
from config import load_config

def launch_vscode(directory):
    subprocess.run(['code', directory])

def launch_jupyter_lab(directory):
    subprocess.run(['jupyter', 'lab', '--notebook-dir', directory])

def main():
    parser = argparse.ArgumentParser(description='Launch coding setup.')
    parser.add_argument('--directory', type=str, help='Directory to launch the coding setup in.')
    parser.add_argument('--conda-env', type=str, help='Conda environment to activate.')

    args = parser.parse_args()

    config = load_config()

    directory = args.directory if args.directory else config['default_directory']
    conda_env = args.conda_env if args.conda_env else config['default_conda_env']

    if conda_env:
        activate_conda_env(conda_env)

    launch_vscode(directory)
    launch_jupyter_lab(directory)

if __name__ == '__main__':
    main()