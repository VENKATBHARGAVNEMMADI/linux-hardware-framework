import subprocess


def check_pcie():
    result = subprocess.run(
        ["lspci"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("PCIe enumeration: FAILED")
        print("Result: FAIL")
        return False

    devices = [
        line for line in result.stdout.splitlines()
        if line.strip()
    ]

    device_count = len(devices)

    print(f"PCI/PCIe devices detected: {device_count}")

    if device_count > 0:
        print("PCIe enumeration: SUCCESS")
        print("Result: PASS")
        return True
    else:
        print("PCIe enumeration: NO DEVICES FOUND")
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_pcie()