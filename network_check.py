import json
import subprocess
from pathlib import Path

from diagnostics import collect_network_diagnostics


def check_network():
    # Load validation requirements
    config = json.loads(Path("config.json").read_text())

    interface = config["network"]["interface"]

    # Check whether the interface exists
    result = subprocess.run(
        ["ip", "link", "show", interface],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Interface {interface}: NOT FOUND")
        print("Result: FAIL")
        collect_network_diagnostics()
        return False

    print(f"Interface {interface}: FOUND")

    # Check whether the interface is UP
    interface_up = "UP" in result.stdout

    if interface_up:
        print(f"Interface {interface} state: UP")
    else:
        print(f"Interface {interface} state: DOWN")

    # Check IPv4 address
    ip_result = subprocess.run(
        ["ip", "-4", "addr", "show", interface],
        capture_output=True,
        text=True
    )

    ipv4_address = None

    for line in ip_result.stdout.splitlines():
        line = line.strip()

        if line.startswith("inet "):
            parts = line.split()
            ipv4_address = parts[1].split("/")[0]
            break

    if ipv4_address is not None:
        print(f"IPv4 address: {ipv4_address}")
    else:
        print("IPv4 address: NOT FOUND")

    # Final network validation
    if interface_up and ipv4_address is not None:
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        collect_network_diagnostics()
        return False


if __name__ == "__main__":
    check_network()