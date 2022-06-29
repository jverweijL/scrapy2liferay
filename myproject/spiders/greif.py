import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import JobItem,GreifItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class GreifSpider(CrawlSpider):
    name = 'greif'
    allowed_domains = ['greif.com']
    start_urls = ['https://www.greif.com/about-greif/news/news/greif-packaging-news']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://www.greif.com/about-greif/news/news/article/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=GreifItem(), response=response)
        #l.add_value('url',response.url)
        l.add_xpath('title', '//h1[1]')
        l.add_xpath('content','//section[@id="news"]/div[3]/div[3]')
        #l.add_value('content','mijn content')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass