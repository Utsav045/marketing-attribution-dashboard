import sys

print("Python executable:", sys.executable)
print("\nFirst 5 entries in sys.path:")
for p in sys.path[:5]:
    print(p)

import src
print("\nImported src from:", src.__file__)