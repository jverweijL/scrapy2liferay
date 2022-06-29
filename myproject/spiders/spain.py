import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import CityItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class SpainSpider(CrawlSpider):
    name = 'spain'
    allowed_domains = ['spain.info']
    start_urls = ['https://www.spain.info/en/search-results/?reloaded&q=*&page=1&rpp=36&typeFilter=SEG-TUR-Destino',
                    'https://www.spain.info/en/search-results/?q=*',
                    'https://www.spain.info/en/search-results/?reloaded&q=*&page=2&rpp=36&typeFilter=SEG-TUR-Destino',
                    'https://www.spain.info/en/search-results/?reloaded&q=*&page=3&rpp=36&typeFilter=SEG-TUR-Destino',
                    'https://www.spain.info/en/search-results/?reloaded&q=*&page=4&rpp=36&typeFilter=SEG-TUR-Destino',
                    'https://www.spain.info/en/search-results/?reloaded&q=*&page=5&rpp=36&typeFilter=SEG-TUR-Destino',
                    'https://www.spain.info/en/search-results/?reloaded&q=*&page=6&rpp=36&typeFilter=SEG-TUR-Destino']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/changeme'),allow=('https://www.spain.info/en/destination/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        l = BasicItemLoader(item=CityItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('title', '//title[1]')
        if response.xpath('//p[contains(@class,"subtitle")][1]/text()').get() is None:
            l.add_value('subtitle','tbd')
        else:
            l.add_xpath('subtitle','//p[contains(@class,"subtitle")][1]/text()')
        #l.add_xpath('name','//h1.titulo-portada[1]/text()')
        l.add_xpath('city','//h1[contains(@class,"titulo-portada")][1]/text()')
        l.add_xpath('intro','//p[@class="text-destacado"][1]/text()')
        l.add_xpath('content','//*[contains(@class, "text-secundario")]')
        #l.add_value('content','mijn content')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass

    