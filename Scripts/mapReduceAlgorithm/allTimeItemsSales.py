import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    if not row:
        continue

    if row[0] == "transaction_id":
        continue

    try:
        store_id = int(row[2])
        product_id = int(row[4])
        quantity = int(row[1])

        key = f"{store_id}|{product_id}"

        print(f"{key}\t{quantity:.2f}")

    except Exception:
        continue