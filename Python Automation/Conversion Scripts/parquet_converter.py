import pandas as pd

data_struct = pd.read_csv("./IKEA_product_catalog.csv")
data_struct.to_parquet(
	"IKEA_product_catalog.snappy.parquet",
	engine="auto",
	compression="snappy"
)
