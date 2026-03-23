import scrapy

class DynamicSpider(scrapy.Spider):
    name = "dynamic"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                }
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        # Wait for dynamic content
        await page.wait_for_timeout(3000)

        title = await page.title()

        # Example: grab all text
        content = await page.content()

        yield {
            "url": response.url,
            "title": title,
            "content": content[:500]  # preview
        }

        await page.close()