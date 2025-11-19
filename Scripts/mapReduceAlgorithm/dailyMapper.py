import sys
import csv
from datetime import datetime

reader = csv.reader(sys.stdin)

for row in reader:
    if row[0] == "transaction_id":
        continue

    # Now we assume this is a real data row in the format:
    # 0: transaction_id
    # 1: transaction_qty
    # 2: store_id
    # 3: store_location
    # 4: product_id
    # 5: unit_price
    # 6: product_category
    # 7: product_type
    # 8: dateAndTimeForTransaction  (YYYY-MM-DD HH:MM:SS)

    try:
        store_id = row[2]
        quantity = int(row[1])
        price = float(row[5])
        time = datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S")

        revenue = price * quantity

        groupedDays = time.strftime("%Y-%m-%d")

        key = f"{store_id}|{groupedDays}"

        print(f"{key}\t{revenue:.2f}")

    except Exception:
        continue
