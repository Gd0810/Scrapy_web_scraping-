import scrapy


class DynamicSpider(scrapy.Spider):
    name = "dynamic"

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
    }

    def __init__(self, url=None, results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.results = results

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            await page.wait_for_timeout(3000)

        title = await page.title()
        html = await page.content()

        item = {
            "title": title,
            "url": response.url,
            "content": html[:2000],
            "mode": "dynamic",
        }

        if self.results is not None:
            self.results.append(item)

        await page.close()

        yield item
