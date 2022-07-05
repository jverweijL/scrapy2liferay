import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import DoctorItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class SpainSpider(CrawlSpider):
    name = 'doctor'
    allowed_domains = ['zorgkaartnederland.nl']
    start_urls = ['https://www.zorgkaartnederland.nl/huisarts']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://www.zorgkaartnederland.nl/zorgverlener/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=DoctorItem(), response=response)
        l.add_value('url',response.url)
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass

    