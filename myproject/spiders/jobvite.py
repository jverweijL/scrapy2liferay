import scrapy
import logging
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from ..itemloaders import SearchDemoLoader
from ..items import JobItem

#mylogger = logging.basicConfig(filename="log.txt",level=logging.DEBUG)

class ExampleSpider(CrawlSpider):
    name = 'jobvite'
    allowed_domains = ['jobvite.com']
    start_urls = ['http://jobs.jobvite.com/liferay']

    rules = (
        Rule(LxmlLinkExtractor(deny=('.*/apply'),allow=('http://jobs.jobvite.com/liferay/job/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('parse_item URL: %s', response.url)
 
        jobtitle = response.xpath('//h2[1]/text()')
        self.logger.info('jobtitle: %s', jobtitle.extract())
        l = SearchDemoLoader(item=JobItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('jobtitle', '//h2[1]/text()')
        l.add_xpath('department', '//h3[1]/text()[1]')
        l.add_xpath('location', '//h3[1]/text()[2]')
        l.add_xpath('content','//div[contains(@class, "jv-job-detail-description")]')
        #l.add_xpath('pubdate','/html/head/meta[@http-equiv="Expires"]/@content')
        #l.add_xpath('content','//div[@id="article"]')
        
        #l.add_xpath('content', '//div[@id="content"]/form/descendant::*/text()')
        #l.add_xpath('cpv', '//dt[text()="Hoofdcategorie:"]/following-sibling::dd/text()')
        return l.load_item()

    def parse(self, response):
        self.logger.info('parse URL: %s', response.url)
        pass