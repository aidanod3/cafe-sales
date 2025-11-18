import sys

currentKey = None
currentSum = 0.0

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue

    key, value_str = parts

    try:
        value = float(value_str)
    except ValueError:
        continue

    if key == currentKey:
        currentSum += value
    else:
        if currentKey is not None:
            print(f"{currentKey}\t{currentSum}")

        currentKey = key
        currentSum = value

if currentKey is not None:
    print(f"{currentKey}\t{currentSum}")
