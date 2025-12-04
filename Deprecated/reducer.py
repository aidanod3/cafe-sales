#!/usr/bin/env python3
import sys

current_key = None
daily_revenue = 0.0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t')
    revenue = float(value)

    if current_key == key:
        daily_revenue += revenue
    else:
        if current_key:
            print(f"{current_key}\t{daily_revenue:.2f}")
        current_key = key
        daily_revenue = revenue

# Print last key
if current_key:
    print(f"{current_key}\t{daily_revenue:.2f}")
