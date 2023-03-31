import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import KlmHealthItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class SpainSpider(CrawlSpider):
    name = 'klmhealth'
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT':50
    }
    allowed_domains = ['klmhealthservices.com']
    start_urls = ['https://www.klmhealthservices.com/reisvoorbereiding/informatie-per-regio-land/'
                    ]

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://klmhealthservices.com/inentingen/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=KlmHealthItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('title', '//title[1]')
        l.add_xpath('content','//*[contains(@class, "wpb_text_column wpb_content_element")]')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass

    