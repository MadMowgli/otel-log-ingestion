import subprocess
from pathlib import Path

script_dir = Path(__file__).resolve().parent
venv_pip = script_dir.parent.parent / ".venv/bin/pip"
requirements_file = script_dir.parent / "requirements.txt"

# update dependency list
with open(requirements_file, "w") as f:
    subprocess.run([venv_pip, "freeze"], stdout=f, check=True)


# update the version
mode = "patch"
version = ""
with open(script_dir / ".version", "w+") as file:
    version = file.read().strip().split(".")
    print('Current version:', version)
    if mode == "major":
        version[0] = str(int(version[0]) + 1)
    if mode == "minor":
        version[1] = str(int(version[1]) + 1)
    if mode == "patch":
        version[2] = str(int(version[2]) + 1)
    print('New version:', version)
    file.write(".".join(version))

# get the latest git commit hash
git_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

# build the image
result = subprocess.run([
    "docker", "build", 
    "-t", "otel-logs-ingestion-app:latest",
    "-t", f'otel-logs-ingestion-app:{str(version)}',
    "-t", f'otel-logs-ingestion-app:{git_commit_hash}'
    "-f", str(script_dir.parent / "DOCKERFILE"),
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
