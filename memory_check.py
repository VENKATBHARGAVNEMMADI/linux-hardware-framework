import json
from pathlib import Path


def check_memory():
    # Load validation requirements
    config = json.loads(Path("config.json").read_text())

    minimum_memory_gib = config["memory"]["minimum_gib"]

    # Read Linux memory information
    meminfo = Path("/proc/meminfo").read_text()

    mem_gib = None

    for line in meminfo.splitlines():
        if line.startswith("MemTotal:"):
            parts = line.split()
            mem_kb = int(parts[1])
            mem_gib = mem_kb / 1024 / 1024
            break

    if mem_gib is None:
        print("Unable to determine system memory")
        print("Result: FAIL")
        return False

    print(f"Required memory: >= {minimum_memory_gib:.2f} GiB")
    print(f"Detected memory: {mem_gib:.2f} GiB")

    if mem_gib >= minimum_memory_gib:
        print("Result: PASS")
        return True
    else:
        print("Result: FAIL")
        return False


if __name__ == "__main__":
    check_memory()