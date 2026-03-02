from utils.data_utils import write_parquet_file
import pandas as pd

class ExportPipe:

    def open_spider(self, spider):
        self.records = []

    def process_item(self, item, spider):
        self.records.append(dict(item))
        return item

    def close_spider(self, spider):
        if self.records:
            df = pd.DataFrame(self.records)
            write_parquet_file(df, "output.parquet")