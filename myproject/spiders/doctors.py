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
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT':1000
    }
    allowed_domains = ['zorgkaartnederland.nl']
    start_urls = ['https://www.zorgkaartnederland.nl/huisarts','https://www.zorgkaartnederland.nl/huisarts/pagina2','https://www.zorgkaartnederland.nl/huisarts/pagina3']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme','.*/waardering','.*/waardeer',',*/wijzig'),allow=('https://www.zorgkaartnederland.nl/zorgverlener/[\w+,-]')), callback='parse_item', follow=True),
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://www.zorgkaartnederland.nl/huisarts/pagina\d+')), callback='parse', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=DoctorItem(), response=response)
        l.add_value('url',response.url)
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass

    