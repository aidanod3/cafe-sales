import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]


originalDataPath = root / "Data" / "rawData" / "coffee_shop_sales.csv"
lookupTable = root / "Data" / "processedData" / "lookupTable.csv"

df = pd.read_csv(originalDataPath)

columns = ["product_id", "product_detail"]
df = df[columns]

df["product_detail"] = df["product_detail"].astype(str).str.strip()
lookup = df.drop_duplicates(subset=["product_id"], keep="first").reset_index(drop=True)

lookup["product_id"] = lookup["product_id"].astype(int)

lookup["product_detail"] = lookup["product_detail"].astype(str)

lookup.to_csv(lookupTable, index=False)

