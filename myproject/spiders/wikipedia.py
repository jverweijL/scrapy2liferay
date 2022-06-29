import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import BasicItemLoader
from ..items import WikipediaItem
from jsonpath_ng import jsonpath, parse
import urllib


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['mediawiki.org','wikipedia.org','wikimedia.org']
    start_urls = ['https://en.wikipedia.org/w/api.php?limit=50&origin=*&action=opensearch&search=starwars']
    
    #def start_requests(self):
    #    yield scrapy.Request('https://api.wikimedia.org/core/v1/wikipedia/en/search/page?q=apple&limit=50', self.parse)

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        #self.logger.info(response.json())

        jsonresponse = response.json()

        jsonpath_expression = parse("$.[1].[*]")
        for match in jsonpath_expression.find(jsonresponse):
            self.logger.info(match.value);
            item_url = 'https://en.wikipedia.org/w/api.php?format=json&redirects=true&action=query&prop=extracts&titles=' + urllib.parse.quote(str(match.value))
            self.logger.info('parse title: %s', item_url)

            yield scrapy.Request(item_url, self.parse_item)
            self.logger.info('yielded')

    def parse_item(self,response):
        self.logger.info('parse item URL: %s', response.url)
        jsonresponse = response.json()
        jsonpath_expression = parse("$.query.pages.*.title")
        titles = jsonpath_expression.find(jsonresponse)
        self.logger.info('parse item title: %s', titles[0].value)
        
        jsonpath_expression = parse("$.query.pages.*.extract")
        extract = jsonpath_expression.find(jsonresponse)
        self.logger.info('parse item extract: %s', extract[0].value)

        l = BasicItemLoader(item=WikipediaItem(), response=response)
        l.add_value('title',titles[0].value)
        l.add_value('content',extract[0].value)
        return l.load_item()

