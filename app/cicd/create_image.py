import subprocess
from pathlib import Path

try:
    script_dir = Path(__file__).resolve().parent
    venv_pip = script_dir.parent.parent / ".venv/bin/pip"
    requirements_file = script_dir.parent / "requirements.txt"

    # update dependency list
    with open(requirements_file, "w") as f:
        subprocess.run([venv_pip, "freeze"], stdout=f, check=True)


    # update the version
    mode = "patch"
    version = ""
    with open(script_dir / ".version", "r") as file:
        version = file.read().strip().split(".")
        print('Current version:', version)
        if mode == "major":
            version[0] = str(int(version[0]) + 1)
        if mode == "minor":
            version[1] = str(int(version[1]) + 1)
        if mode == "patch":
            version[2] = str(int(version[2]) + 1)
        version = ".".join(version)
        print('New version:', version)

    # get the latest git commit hash
    git_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    print('Git commit hash:', git_commit_hash)

    # build the image
    result = subprocess.run([
        "docker", "build", 
        "-t", "otel-logs-ingestion-app:latest",
        "-t", f'otel-logs-ingestion-app:{str(version)}',
        "-t", f'otel-logs-ingestion-app:{git_commit_hash}',
        "-f", str(script_dir.parent / "Dockerfile"),
        str(script_dir.parent)
    ], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    # load the image into minikube after removing it first
    subprocess.run(["minikube", "image", "rm", "otel-logs-ingestion-app:latest"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print("Old image removed from minikube.")
    result = subprocess.run(["minikube", "image", "load", "otel-logs-ingestion-app:latest"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print("Image built and loaded into minikube successfully.")

    
except Exception as e:
    print("Error:", e)
    exit(1)

# only now commit the version update, since everything went smooth
with open(script_dir / ".version", "w") as file:
    file.write(version)