import subprocess

repo_path = "/home/luke/PycharmProjects/testing"

# Spuštění příkazu git log pomocí subprocess
result = subprocess.run(
    ["git", "log", "--pretty=format:%h %s", "--reverse"],
    cwd=repo_path,
    capture_output=True,
    text=True,
)

hashes = [x.split(" ")[0] for x in result.stdout.split("\n")]
print(hashes)