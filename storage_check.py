import json
import subprocess
from pathlib import Path


def check_storage():
    # Load validation requirements
    config = json.loads(Path("config.json").read_text())

    maximum_usage = config["storage"]["maximum_usage_percent"]

    # Check root filesystem usage
    result = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True,
        check=True
    )

    lines = result.stdout.splitlines()
    parts = lines[1].split()

    usage = int(parts[4].replace("%", ""))

    print(f"Root filesystem usage: {usage}%")
    print(f"Maximum allowed usage: {maximum_usage}%")

    if usage < maximum_usage:
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_storage()