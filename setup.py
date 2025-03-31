from setuptools import setup, find_packages

setup(
    name='coding-setup-tool',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A command line tool to quickly launch coding setups with VS Code and Jupyter Lab.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',  # For command line argument parsing
        'subprocess32',  # For subprocess management (if using Python 2.7)
        'jupyterlab',  # For Jupyter Lab support
    ],
    entry_points={
        'console_scripts': [
            'coding-setup=coding_setup_tool.main:main',  # Entry point for the command line tool
        ],
    },
)