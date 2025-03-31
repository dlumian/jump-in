def conda_env_exists(env_name):
    import subprocess

    try:
        result = subprocess.run(
            ["conda", "env", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return env_name in result.stdout
    except subprocess.CalledProcessError:
        return False

def activate_conda_env(env_name):
    import os
    import subprocess

    if conda_env_exists(env_name):
        activate_script = f"conda activate {env_name}"
        os.system(activate_script)
    else:
        raise ValueError(f"Conda environment '{env_name}' does not exist.")

def launch_vscode(directory):
    import subprocess

    subprocess.run(["code", directory])

def launch_jupyter_lab(directory):
    import subprocess

    subprocess.run(["jupyter", "lab", "--notebook-dir", directory])