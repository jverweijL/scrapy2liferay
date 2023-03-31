import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import vmo2Item

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class Vmo2Spider(CrawlSpider):
    name = 'vmo2'
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT':500
    }
    allowed_domains = ['virginmediabusiness.co.uk']
    start_urls = ['https://www.virginmediabusiness.co.uk/wholesale/content-hub/news-and-insights/',
    'https://www.virginmediabusiness.co.uk/small-business/insights/',
    'https://www.virginmediabusiness.co.uk/enterprise-and-public-sector-insights/']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://www.virginmediabusiness.co.uk/insights/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=vmo2Item(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('title', '//title[1]')
        l.add_xpath('content','//*[contains(@class, "richtext")]')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass

    