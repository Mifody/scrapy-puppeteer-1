import scrapy

from scrapypuppeteer import PuppeteerRequest, PuppeteerResponse
from scrapypuppeteer.actions import Goto


class TestSpider(scrapy.Spider):
    name = 'meduza'

    def start_requests(self):
        yield PuppeteerRequest(Goto('https://meduza.io'), callback=self.parse_main_page)

    def parse_main_page(self, response: PuppeteerResponse):
        for article_url in response.css('a.Link-isInBlockTitle::attr(href)').getall():
            yield response.follow(Goto(article_url), callback=self.parse_article)

    def parse_article(self, response: PuppeteerResponse):
        yield {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'text': '\n'.join(response.css('p.SimpleBlock-p::text').getall())
        }
