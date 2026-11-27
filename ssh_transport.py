import subprocess


class SSHTransport:
    def __init__(self, host, username, timeout=5):
        self.host = host
        self.username = username
        self.timeout = timeout

    def run_command(self, command):
        target = f"{self.username}@{self.host}"

        print(f"SSH target: {target}")
        print(f"Remote command: {command}")

        try:
            result = subprocess.run(
                [
                    "ssh",
                    "-o", "BatchMode=yes",
                    "-o", f"ConnectTimeout={self.timeout}",
                    target,
                    command
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout + 2
            )

        except subprocess.TimeoutExpired:
            print("SSH connection: TIMEOUT")
            return None

        if result.returncode != 0:
            print("SSH command: FAILED")

            if result.stderr:
                print(f"Error: {result.stderr.strip()}")

            return None

        output = result.stdout.strip()

        print(f"Remote output: {output}")
        return output


if __name__ == "__main__":
    transport = SSHTransport(
        host="localhost",
        username="zahazshaik1998",
        timeout=5
    )

    output = transport.run_command("uname -a")

    if output is not None:
        print("SSH Validation: PASS")
    else:
        print("SSH Validation: FAIL")