import json
import os
from pathlib import Path

#check the cpu for testing


def check_cpu():
    # Load validation requirements
    config = json.loads(Path("config.json").read_text())

    minimum_cpu_count = config["cpu"]["minimum_count"]

    # Detect available CPUs
    cpu_count = os.cpu_count()

    print(f"Required CPUs: >= {minimum_cpu_count}")
    print(f"Detected CPUs: {cpu_count}")

    if cpu_count is not None and cpu_count >= minimum_cpu_count:
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_cpu()