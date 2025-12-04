import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]


originalDataPath = root / "Data" / "rawData" / "coffee_shop_sales.csv"
lookupTablePath  = root / "Data" / "processedData" / "lookupTableDetailed.csv"


df = pd.read_csv(originalDataPath)


lookup = df[[
    "product_id",
    "product_category",
    "product_type",
    "product_detail"
]].copy()


lookup["product_id"] = lookup["product_id"].astype(int)
lookup["product_category"] = lookup["product_category"].astype(str)
lookup["product_type"] = lookup["product_type"].astype(str)
lookup["product_detail"] = lookup["product_detail"].astype(str)


lookup = lookup.drop_duplicates().sort_values("product_id")


lookup.to_csv(lookupTablePath, index=False)