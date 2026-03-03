import scrapy


class CrawlSpider(scrapy.Spider):
    name = "crawl_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.records = []

    def parse(self, response):
        for book in response.css("article.product_pod"):
            title = book.css("h3 a::attr(title)").get()
            price = book.css("p.price_color::text").get()
            rating_class = book.css("p.star-rating::attr(class)").get()

            rating = (
                rating_class.replace("star-rating", "").strip()
                if rating_class else None
            )

            yield {
                "title": title,
                "price": price,
                "rating": rating
            }

        # paginate
        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)