from scrapy.crawler import CrawlerProcess
from .spider import CrawlSpider



def run_spider(start_url: str):
    process = CrawlerProcess({
        "LOG_LEVEL": "INFO",
        "USER_AGENT": "DataExtractBot/1.0",
        "ITEM_PIPELINES": {
        "scrappers.extractpipe.ExportPipe": 300,
    },
    })
    process.crawl(CrawlSpider, start_url=start_url)
    process.start()


if __name__ == "__main__":
    run_spider("https://books.toscrape.com/")