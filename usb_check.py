import subprocess
from pathlib import Path


def check_usb():
    result = subprocess.run(
        ["lsusb"],
        capture_output=True,
        text=True
    )

    # Detect whether we are running inside WSL
    kernel_info = Path("/proc/version").read_text().lower()
    running_in_wsl = "microsoft" in kernel_info

    if result.returncode != 0:
        if running_in_wsl:
            print("USB enumeration unavailable in current WSL environment")
            print("Result: SKIP")
            return None
        else:
            print("USB enumeration: FAILED")
            print("Result: FAIL")
            return False

    devices = [
        line for line in result.stdout.splitlines()
        if line.strip()
    ]

    print(f"USB devices detected: {len(devices)}")
    print("USB enumeration: SUCCESS")
    print("Result: PASS")
    return True


if __name__ == "__main__":
    check_usb()