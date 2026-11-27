import sys


def process_command(command):
    command = command.strip().upper()

    if command == "STATUS":
        return "OK"

    elif command == "GET_TEMP":
        return "TEMP:42"

    elif command == "GET_VERSION":
        return "VERSION:1.0"

    else:
        return "ERROR:UNKNOWN_COMMAND"


if __name__ == "__main__":
    command = sys.stdin.readline()

    if command:
        response = process_command(command)
        print(response)