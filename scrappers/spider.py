import scrapy
import pandas as pd


class TableSpider(scrapy.Spider):
    name = "table_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.records = []

    def parse(self, response):
        tables = response.css("table")

        for table in tables:
            headers = table.css("th::text").getall()
            rows = table.css("tr")

            for row in rows[1:]:
                values = row.css("td::text").getall()
                if len(values) == len(headers):
                    record = dict(zip(headers, values))
                    self.records.append(record)

    def closed(self, reason):
        df = pd.DataFrame(self.records)
        df.to_json("scraped_data.json", orient="records", indent=2)