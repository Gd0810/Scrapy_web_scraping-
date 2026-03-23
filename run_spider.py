from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.dynamic_spider import DynamicSpider

def run_spider(url):
    process = CrawlerProcess(get_project_settings())

    results = []

    class ResultSpider(DynamicSpider):
        def parse(self, response):
            for item in super().parse(response):
                results.append(item)
                yield item

    process.crawl(ResultSpider, url=url)
    process.start()

    return results