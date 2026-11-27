import serial


class SerialTransport:
    def __init__(self, port, baud_rate=115200, timeout=2):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.timeout
            )

            print(f"Serial port connected: {self.port}")
            print(f"Baud rate: {self.baud_rate}")
            return True

        except serial.SerialException as error:
            print(f"Serial connection failed: {error}")
            return False

    def send_command(self, command):
        if self.connection is None or not self.connection.is_open:
            print("Cannot send command: serial port is not connected")
            return None

        try:
            # TX: send command to DUT
            message = command + "\n"
            self.connection.write(message.encode("utf-8"))

            print(f"TX: {command}")

            # RX: wait for DUT response
            response = self.connection.readline()

            if not response:
                print("RX: TIMEOUT")
                return None

            decoded_response = response.decode("utf-8").strip()

            print(f"RX: {decoded_response}")
            return decoded_response

        except serial.SerialException as error:
            print(f"Serial communication error: {error}")
            return None

    def disconnect(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()
            print("Serial connection closed")


if __name__ == "__main__":
    transport = SerialTransport(
        port="/dev/ttyUSB0",
        baud_rate=115200,
        timeout=2
    )

    if transport.connect():
        transport.send_command("STATUS")
        transport.disconnect()