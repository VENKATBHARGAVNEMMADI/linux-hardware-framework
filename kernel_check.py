import subprocess
from pathlib import Path


def check_kernel():
    result = subprocess.run(
        ["dmesg"],
        capture_output=True,
        text=True
    )

    # If dmesg is unavailable, skip this test
    if result.returncode != 0:
        print("Kernel log access: FAILED")
        print("Result: SKIP")
        return None

    # Keywords that may indicate kernel or driver problems
    keywords = [
        "error",
        "fail",
        "timeout",
        "i/o"
    ]

    # Known WSL/WSLg and normal boot messages observed
    known_wsl_noise = [
        "checkconnection: getaddrinfo() failed",
        "dxgk:",
        "failed to connect to system scope bus via local transport",
        "rdp-backend.so",
        "failed to register legacy timer interrupt",
        "apic: switch to symmetric i/o mode setup",
        "ras: correctable errors collector initialized"
    ]

    suspicious_lines = []
    ignored_lines = []

    # Analyze the kernel log
    for line in result.stdout.splitlines():
        lower_line = line.lower()

        if any(keyword in lower_line for keyword in keywords):
            if any(noise in lower_line for noise in known_wsl_noise):
                ignored_lines.append(line)
            else:
                suspicious_lines.append(line)

    print(f"Kernel warning/error matches: {len(suspicious_lines)}")
    print(f"Known WSL messages ignored: {len(ignored_lines)}")

    # Create log directory
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "kernel_diagnostics.log"

    # Save diagnostic evidence
    with log_file.open("w") as file:
        file.write("===== KERNEL DIAGNOSTICS =====\n\n")

        file.write("Suspicious messages:\n")

        if suspicious_lines:
            for line in suspicious_lines:
                file.write(line + "\n")
        else:
            file.write("None\n")

        file.write("\nKnown WSL messages ignored:\n")

        if ignored_lines:
            for line in ignored_lines:
                file.write(line + "\n")
        else:
            file.write("None\n")

    print(f"Diagnostics saved to: {log_file}")

    # Final validation decision
    if len(suspicious_lines) == 0:
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_kernel()