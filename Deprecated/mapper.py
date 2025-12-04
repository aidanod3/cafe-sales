#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        # parse csv line
        fields = next(csv.reader([line]))
        if fields[0] == 'transaction_id':
            continue  # skip header

        transaction_date = fields[1]
        store_id = fields[4]
        transaction_qty = int(fields[3])
        unit_price = float(fields[7])
        revenue = transaction_qty * unit_price

        # emit key-value pair
        print(f"{transaction_date}|{store_id}\t{revenue:.2f}")
    except Exception:
        continue  # skip bad rows
