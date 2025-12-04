import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]

originalDataPath = root / "Data" / "rawData" / "coffee_shop_sales.csv"
lookupTable = root / "Data" / "processedData" / "lookupTable.csv"

# load file
df = pd.read_csv(originalDataPath)

# select related columns
lookup = df[["product_id", "product_type", "product_category"]].copy()

# drop duplicates
lookup = lookup.drop_duplicates().sort_values("product_id")

# ensure types
lookup["product_id"] = lookup["product_id"].astype(int)
lookup["product_category"] = lookup["product_category"].astype(str)
lookup["product_type"] = lookup["product_type"].astype(str)

# save table
lookup.to_csv(lookupTable, index=False)