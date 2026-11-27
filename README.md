# Linux Hardware & System Validation Framework

A Python-based validation framework for automating Linux system checks, DUT communication, diagnostics, remote execution, and validation reporting.

## Features

- CPU and memory validation
- Storage usage validation
- Network interface validation
- PCI/PCIe device enumeration
- USB enumeration with WSL-aware SKIP handling
- Kernel and driver log analysis
- Automated diagnostic log collection
- PASS / FAIL / SKIP result classification
- Configuration-driven validation requirements
- Simulated DUT command/response testing
- Timeout and retry handling
- Fault-injection testing
- Serial/UART communication using PySerial
- Configurable simulated and serial DUT modes
- SSH remote command execution
- Key-based SSH authentication
- Automated tests using pytest
- Timestamped validation reporting

## Architecture

Validation checks are executed by a central runner:

    run_validation.py
           |
           +-- System Validation
           |     +-- Memory
           |     +-- CPU
           |     +-- Storage
           |     +-- Network
           |     +-- PCIe
           |     +-- USB
           |     +-- Kernel / Driver
           |
           +-- DUT Validation
           |     +-- Simulated DUT
           |     +-- Serial / UART Transport
           |
           +-- Remote Validation
           |     +-- SSH Transport
           |
           +-- Diagnostics & Reporting

## Technologies

- Python
- Linux / WSL2
- PySerial
- OpenSSH
- pytest
- Git

## Installation

Create and activate a Python virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

## Run Validation

    python3 run_validation.py

The framework executes the configured validation checks and produces an overall PASS/FAIL result.

## Run Automated Tests

    python -m pytest -v

## Configuration

Validation requirements and DUT communication settings are stored in:

    config.json

The DUT can operate in simulated mode for development or serial mode for communication with a compatible physical target.

## Diagnostics

Failure diagnostics are written to the `logs/` directory during execution.

Validation summaries are written to the `reports/` directory.

These generated files are excluded from Git.

## Environment Notes

This project was developed and tested using Ubuntu under WSL2.

Some hardware interfaces exposed to native Linux systems may not be directly available through WSL2. USB validation therefore supports an environment-aware SKIP result rather than reporting an artificial PASS.

The serial/UART transport has been implemented with PySerial and its failure behavior has been tested without a connected physical UART DUT. Physical board-level UART validation requires compatible hardware.

SSH remote-execution behavior was validated using a local SSH server as a controlled Linux target.

## Testing Approach

The framework was tested using both successful and deliberately failing conditions, including:

- Invalid network interface
- Unexpected DUT response
- DUT retry behavior
- Serial device unavailable
- SSH target unavailable
- Kernel-log filtering
- Unknown simulated-DUT commands

This allows the framework to exercise detection, failure handling, diagnostic collection, and recovery behavior rather than validating only successful paths.