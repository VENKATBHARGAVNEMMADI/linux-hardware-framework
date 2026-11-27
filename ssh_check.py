import json
from pathlib import Path

from ssh_transport import SSHTransport


def check_ssh():
    config = json.loads(Path("config.json").read_text())
    ssh_config = config["ssh"]

    if not ssh_config["enabled"]:
        print("Remote SSH validation disabled")
        print("Result: SKIP")
        return None

    transport = SSHTransport(
        host=ssh_config["host"],
        username=ssh_config["username"],
        timeout=ssh_config["timeout"]
    )

    print("Running remote Linux validation...")

    output = transport.run_command("uname -s")

    if output == "Linux":
        print("Remote operating system: Linux")
        print("Result: PASS")
        return True

    print("Remote Linux validation failed")
    print("Result: FAIL")
    return False


if __name__ == "__main__":
    check_ssh()