from simulated_dut import process_command


def test_status_command():
    response = process_command("STATUS")
    assert response == "OK"


def test_temperature_command():
    response = process_command("GET_TEMP")
    assert response == "TEMP:42"


def test_version_command():
    response = process_command("GET_VERSION")
    assert response == "VERSION:1.0"


def test_unknown_command():
    response = process_command("HELLO")
    assert response == "ERROR:UNKNOWN_COMMAND"


def test_lowercase_command():
    response = process_command("status")
    assert response == "OK"


def test_command_with_spaces():
    response = process_command("  STATUS  ")
    assert response == "OK"