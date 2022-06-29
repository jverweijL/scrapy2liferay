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
    name = 'brickr.nl'
    allowed_domains = ['brickr.nl']
    start_urls = ['https://www.brickr.nl/zoeken?controller=search&s=lego&order=product.position.desc&resultsPerPage=9999999']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/apply'),allow=('https://www.brickr.nl/home/.*\.html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)

        l = LegoItemLoader(item=LegoItem(), response=response)
        l.add_value('shop','brickr')
        l.add_value('url',response.url)
        l.add_xpath('legoid', '//title')
        l.add_xpath('price', '//meta[@property="product:price:amount"]/@content')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass