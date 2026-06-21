import subprocess
import sys

print("\n================================")
print("RUNNING ALL PROJECT TESTS")
print("================================\n")

test_files = [
    "tests/test_utils.py",
    "tests/test_ingestion.py",
    "tests/test_preprocessing.py"
]

for test in test_files:

    print(f"\nRunning: {test}\n")

    subprocess.run(
        [sys.executable, test],
        check=False
    )

print("\n================================")
print("TEST EXECUTION COMPLETED")
print("================================")