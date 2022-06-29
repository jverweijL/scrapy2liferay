import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import LegoItemLoader
from ..items import LegoItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class LegoSpider(CrawlSpider):
    name = 'misterbricks.nl'
    allowed_domains = ['misterbricks.nl']
    start_urls = ['https://misterbricks.nl/catalogsearch/result/?q=lego']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/apply'),allow=('https://misterbricks.nl/.*\.html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)

        l = LegoItemLoader(item=LegoItem(), response=response)
        l.add_value('shop','misterbricks')
        l.add_value('url',response.url)
        l.add_xpath('legoid', '//title')
        l.add_xpath('price', '//@data-price-amount')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass