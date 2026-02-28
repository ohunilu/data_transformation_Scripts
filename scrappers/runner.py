import pandas as pd
from utils.data_utils import (
    write_csv_file,
    write_avro_file,
    write_parquet_file,
)

df = pd.read_json("scraped_data.json")

write_csv_file(df, "output.csv")
write_avro_file(df, "output.avro")
write_parquet_file(df, "output.parquet")