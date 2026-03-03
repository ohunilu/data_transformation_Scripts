from scrapy.crawler import CrawlerProcess
from .spider import CrawlSpider
from halo import Halo
import logging

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_spider(start_url: str):
    logger.info("Starting spider for URL: %s", start_url)

    spinner = Halo(text="Scraping in progress...", spinner="dots")
    spinner.start()

    process = CrawlerProcess({
        "LOG_ENABLED": False,
        "USER_AGENT": "DataExtractBot/1.0",
        "ITEM_PIPELINES": {
            "scrappers.extractpipe.ExportPipe": 300
        },
    })
    process.crawl(CrawlSpider, start_url=start_url)
    process.start()

    spinner.succeed("Scraping completed successfully!")

    logger.info("Spider finished successfully.")


if __name__ == "__main__":
    run_spider("https://books.toscrape.com/")
