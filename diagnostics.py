import subprocess
from pathlib import Path


def collect_network_diagnostics():
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "network_failure.log"

    commands = [
        ["ip", "addr"],
        ["ip", "link"],
        ["ip", "route"]
    ]

    with log_file.open("w") as file:
        for command in commands:
            file.write(f"\n===== {' '.join(command)} =====\n")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            file.write(result.stdout)

            if result.stderr:
                file.write("\nSTDERR:\n")
                file.write(result.stderr)

    print(f"Diagnostics saved to: {log_file}")


if __name__ == "__main__":
    collect_network_diagnostics()