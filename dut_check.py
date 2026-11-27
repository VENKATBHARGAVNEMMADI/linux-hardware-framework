import json
import subprocess
from pathlib import Path

from serial_transport import SerialTransport


def send_simulated_command(command, expected_response, max_retries=3):
    print(f"\nSending: {command}")

    for attempt in range(1, max_retries + 1):
        print(f"Attempt: {attempt}/{max_retries}")

        try:
            result = subprocess.run(
                ["python3", "simulated_dut.py"],
                input=command + "\n",
                capture_output=True,
                text=True,
                timeout=2
            )

        except subprocess.TimeoutExpired:
            print("DUT response: TIMEOUT")

            if attempt < max_retries:
                print("Retrying...")
                continue

            print("Command Result: FAIL")
            return False

        response = result.stdout.strip()

        print(f"Received: {response}")
        print(f"Expected: {expected_response}")

        if response == expected_response:
            print("Command Result: PASS")
            return True

        print("Unexpected response")

        if attempt < max_retries:
            print("Retrying...")

    print("Command Result: FAIL")
    return False


def check_dut():
    config = json.loads(Path("config.json").read_text())

    dut_config = config["dut"]
    mode = dut_config["mode"]

    print("====== DUT COMMUNICATION TEST ======")
    print(f"Communication mode: {mode}")

    tests = {
        "STATUS": "OK",
        "GET_TEMP": "TEMP:42",
        "GET_VERSION": "VERSION:1.0"
    }

    results = []

    if mode == "simulated":
        for command, expected_response in tests.items():
            result = send_simulated_command(
                command,
                expected_response
            )
            results.append(result)

    elif mode == "serial":
        serial_config = dut_config["serial"]

        transport = SerialTransport(
            port=serial_config["port"],
            baud_rate=serial_config["baud_rate"],
            timeout=serial_config["timeout"]
        )

        if not transport.connect():
            print("Result: FAIL")
            return False

        try:
            for command, expected_response in tests.items():
                response = transport.send_command(command)

                print(f"Expected: {expected_response}")

                if response == expected_response:
                    print("Command Result: PASS")
                    results.append(True)
                else:
                    print("Command Result: FAIL")
                    results.append(False)

        finally:
            transport.disconnect()

    else:
        print(f"Unknown DUT mode: {mode}")
        print("Result: FAIL")
        return False

    print("\n--- DUT Validation Result ---")

    if all(results):
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_dut()