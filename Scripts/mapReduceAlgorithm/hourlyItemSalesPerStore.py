import sys
import csv
from datetime import datetime

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
        datetimeString = datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S")

        datetimeString = datetimeString.replace(minute=0, second=0, microsecond=0)
        hour = datetimeString.strftime("%m-%d %H:%M")
        key = f"{store_id}|{product_id}|{hour}"

        print(f"{key}\t{quantity:.2f}")

    except Exception:
        continue