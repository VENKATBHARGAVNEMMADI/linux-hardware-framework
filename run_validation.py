from pathlib import Path
from datetime import datetime

from memory_check import check_memory
from cpu_check import check_cpu
from storage_check import check_storage
from network_check import check_network
from pcie_check import check_pcie
from usb_check import check_usb
from kernel_check import check_kernel
from dut_check import check_dut
from ssh_check import check_ssh


print("====== SYSTEM VALIDATION ======")

print("\n--- Memory Test ---")
memory_result = check_memory()

print("\n--- CPU Test ---")
cpu_result = check_cpu()

print("\n--- Storage Test ---")
storage_result = check_storage()

print("\n--- Network Test ---")
network_result = check_network()

print("\n--- PCIe Test ---")
pcie_result = check_pcie()

print("\n--- USB Test ---")
usb_result = check_usb()

print("\n--- Kernel / Driver Test ---")
kernel_result = check_kernel()

print("\n--- DUT Communication Test ---")
dut_result = check_dut()

print("\n--- Remote SSH Test ---")
ssh_result = check_ssh()


results = {
    "Memory": memory_result,
    "CPU": cpu_result,
    "Storage": storage_result,
    "Network": network_result,
    "PCIe": pcie_result,
    "USB": usb_result,
    "Kernel / Driver": kernel_result,
    "DUT Communication": dut_result,
    "Remote SSH": ssh_result
}


def status_text(result):
    if result is True:
        return "PASS"
    elif result is False:
        return "FAIL"
    else:
        return "SKIP"


passed_tests = list(results.values()).count(True)
failed_tests = list(results.values()).count(False)
skipped_tests = list(results.values()).count(None)
total_tests = len(results)

if failed_tests == 0:
    overall_result = "PASS"
else:
    overall_result = "FAIL"


print("\n========== SUMMARY ==========")

for test_name, result in results.items():
    print(f"{test_name:<20}: {status_text(result)}")

print("--------------------------------")
print(f"Tests Run : {total_tests}")
print(f"Passed    : {passed_tests}")
print(f"Failed    : {failed_tests}")
print(f"Skipped   : {skipped_tests}")
print(f"Overall   : {overall_result}")
print("================================")


report_directory = Path("reports")
report_directory.mkdir(exist_ok=True)

timestamp = datetime.now()
report_file = report_directory / "validation_summary.txt"

with report_file.open("w") as file:
    file.write("========== SYSTEM VALIDATION REPORT ==========\n")
    file.write(
        f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )

    for test_name, result in results.items():
        file.write(
            f"{test_name:<20}: {status_text(result)}\n"
        )

    file.write("\n---------------- SUMMARY ----------------\n")
    file.write(f"Tests Run : {total_tests}\n")
    file.write(f"Passed    : {passed_tests}\n")
    file.write(f"Failed    : {failed_tests}\n")
    file.write(f"Skipped   : {skipped_tests}\n")
    file.write(f"Overall   : {overall_result}\n")

print(f"\nReport saved to: {report_file}")