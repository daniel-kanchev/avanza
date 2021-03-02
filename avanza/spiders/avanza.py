import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from avanza.items import Article


class AvanzaSpider(scrapy.Spider):
    name = 'avanza'
    start_urls = ['https://www.avanza.se/placera/forstasidan.html']

    def parse(self, response):
        links = response.xpath('//div[@class="cq-puff"]//h1/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="articleTop "]/h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@itemprop="articleBody"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
