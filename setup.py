import os
import subprocess

def create_conda_env(env_name, requirements_file):
    # Create Conda environment
    env_create_cmd = f"conda create --prefix ./{env_name} python=3.8"
    subprocess.run(env_create_cmd, shell=True, check=True)

    # Initialize Conda (if not already initialized)
    conda_init_cmd = "conda init"
    subprocess.run(conda_init_cmd, shell=True, check=True)

    # Activate Conda environment using source command
    activate_cmd = f"source activate ./{env_name}"
    subprocess.run(activate_cmd, shell=True, check=True)

    # Install packages using Conda or pip
    with open(requirements_file, 'r') as file:
        for line in file:
            package = line.strip()
            if package.startswith('#') or not package:
                continue  # Skip comments and empty lines
            try:
                # Try installing using Conda
                conda_install_cmd = f"conda install --yes {package}"
                subprocess.run(conda_install_cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                # If installation using Conda fails, install using pip
                pip_install_cmd = f"pip install {package}"
                subprocess.run(pip_install_cmd, shell=True, check=True)

if __name__ == "__main__":
    env_name = "portfolio_optimization_env"
    requirements_file = "requirements.txt"
    create_conda_env(env_name, requirements_file)
