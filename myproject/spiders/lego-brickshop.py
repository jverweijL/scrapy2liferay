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
    name = 'brickshop.nl'
    allowed_domains = ['brickshop.nl']
    start_urls = ['https://www.brickshop.nl/lego#index.php?option=com_virtuemart&page=shop.filter&f_type=1']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/apply'),allow=('https://www.brickshop.nl/lego/.*')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)

        l = LegoItemLoader(item=LegoItem(), response=response)
        l.add_value('shop','brickshop')
        l.add_value('url',response.url)
        l.add_xpath('legoid', '//meta[@itemprop="sku"]/@content')
        l.add_xpath('price', '//meta[@itemprop="price"]/@content')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass