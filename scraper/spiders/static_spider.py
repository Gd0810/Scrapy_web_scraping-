import scrapy


class StaticSpider(scrapy.Spider):
    name = "static"

    def __init__(self, url=None, results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.results = results

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        title = response.css("title::text").get() or ""
        html = response.text or ""

        item = {
            "title": title.strip(),
            "url": response.url,
            "content": html[:2000],
            "mode": "static",
        }

        if self.results is not None:
            self.results.append(item)

        yield item
