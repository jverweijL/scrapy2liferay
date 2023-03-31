import logging, json, requests, hashlib
import urllib.request, urllib.parse
from datetime import date
from datetime import timedelta
from scrapy.exceptions import DropItem
from .items import JobItem, WikipediaItem, GreifItem, LegoItem, CityItem, vmo2Item, KlmHealthItem
from jsonpath_ng import jsonpath,parse


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

protocol = "http"
host = "localhost"
port = "8080"
username = "admin@liferay.com"
password = "test"
folderId = "0"

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class DataCleanserPipeline(object):
    def process_item(self, item, spider):

        # The title always contains some fixed part
        #item['title'] = item['title'].replace('jan was here','')

        # Clean pubdate since current site is not closing the Expires tag correct
        #if ">" in item['pubdate']:
        #    item['pubdate'] = item['pubdate'].split('>')[0]

        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class JobImportPipeline(object):
    def process_item(self, item, spider):

        folderId = "56594"

        if not type(item) is JobItem:
            return item

        else:            

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['url']
                            },
                            "name": "url"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['department']
                            },
                            "name": "department"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['location']
                            },
                            "name": "location"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "body"
                        }
                    ],
                    "contentStructureId": 57788,
                    "title": item['jobtitle'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

class WikipediaImportPipeline(object):
    def process_item(self, item, spider):

        if not type(item) is WikipediaItem:
            return item

        else:

            folderId = "78289"

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "content"
                        }
                    ],
                    "contentStructureId": 41479,
                    "title": item['title'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)


class KlmHealthImportPipeline(object):
    def process_item(self, item, spider):

        if not type(item) is KlmHealthItem:
            return item

        else:

            folderId = "55504"

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "content"
                        }
                    ],
                    "contentStructureId": 42804,
                    "title": item['title'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

class vmo2ImportPipeline(object):
    def process_item(self, item, spider):

        protocol = "https"
        host = "webserver-lctvmo2-prd.lfr.cloud"
        port = "443"
        username = "admin@vmo2.com"
        password = "Gloria1234!"

        if not type(item) is vmo2Item:
            return item

        else:

            folderId = "47099"

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "content"
                        }
                    ],
                    "contentStructureId": 42225,
                    "title": item['title'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

class CityImportPipeline(object):
    def process_item(self, item, spider):
        
        folderId = "50912"
        structureId = "50902"

        if not type(item) is CityItem:
            return item

        else:           
#
            with urllib.request.urlopen("http://api.positionstack.com/v1/forward?access_key=49e080366f665b75d6edfb67b984a71a&query=" + urllib.parse.quote_plus(item['city']) + ",Spain") as response:
                res = json.loads(response.read())
#
            print(res)
#
            jsonpath_lat = parse('$.data.[0].latitude')
            jsonpath_lon = parse('$.data.[0].longitude')
#
            lat = [match.value for match in jsonpath_lat.find(res)]
            print(lat[0])
            lon = [match.value for match in jsonpath_lon.find(res)]
            print(lon[0])

            
            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['subtitle']
                            },
                            "name": "subtitle"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['intro']
                            },
                            "name": "intro"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "content"
                        },
                        {
                            "contentFieldValue": {
                                "geo": {
                                "latitude": lat[0], 
                                "longitude": lon[0]
                                }
                            },
                            "name": "geo"
                        }
                    ],
                    "contentStructureId": structureId,
                    "title": item['city'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }

            print(payload)

            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

class GreifImportPipeline(object):
    def process_item(self, item, spider):

        if not type(item) is GreifItem:
            return item

        else:

            folderId = "81849"

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['content']
                            },
                            "name": "content"
                        }
                    ],
                    "contentStructureId": 41479,
                    "title": item['title'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }
            
            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

class LegoImportPipeline(object):
    def process_item(self, item, spider):

        if not type(item) is LegoItem:
            return item

        if item['price'] is None:
            return item

        if item['legoid'] is None:
            return item

        else:

            folderId = "88366"

            url = protocol + "://" + host + ":" + port + "/o/headless-delivery/v1.0/structured-content-folders/" + folderId + "/structured-contents"
            payload = json.dumps(
                {
                    "contentFields": [
                        {
                            "contentFieldValue": {
                                "data": item['legoid']
                            },
                            "name": "legoID"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['price']
                            },
                            "name": "price"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['shop']
                            },
                            "name": "shop"
                        },
                        {
                            "contentFieldValue": {
                                "data": item['url']
                            },
                            "name": "url"
                        }
                    ],
                    "contentStructureId": 87727,
                    "title": item['legoid'] + " - " + item['shop'],
                    "viewableBy": "Anyone"
                }
            )
            headers = {
            'Content-Type': 'application/json'
            }
            
            response = requests.request("POST", url, auth=(username, password), headers=headers, data=payload)

## class LiferayArticleImporterPipeline(object):
##     def process_item(self, item, spider):
##         
##         today = date.today()
##         expiredate = today + timedelta(days=30)
##         title = b'{{"en_US":"JOB | {0}"}}'.format(item['jobtitle'])
##         #content = b'<?xml version="1.0"?><root available-locales="en_US" default-locale="en_US"><dynamic-element name="content" type="text_area" index-type="text" instance-id="bbau"><dynamic-content language-id="en_US"><![CDATA[<p>{1}</p><p>{0}</p>]]></dynamic-content></dynamic-element></root>'.format(item['content'].encode('utf8', 'ignore'),item['url'])
##         content = b'<root available-locales="en_US" default-locale="en_US"><dynamic-element name="content" type="text_area" index-type="text" instance-id="wosy"><dynamic-content language-id="en_US"><![CDATA[<p>{0}</p>]]></dynamic-content></dynamic-element><dynamic-element name="URL" type="text" index-type="keyword" instance-id="pyyp"><dynamic-content language-id="en_US"><![CDATA[{1}]]></dynamic-content></dynamic-element></root>'.format(item['content'].encode('utf8', 'ignore'),item['url'])
##         uid = hashlib.md5(item['url'].encode("utf8")).hexdigest()
## 
##         headers = {}
##         payload = {'groupId':groupId,
##                    'folderId':folderId,
##                    'classNameId':0,
##                    'classPK':0,
##                    'articleId':uid,
##                    'autoArticleId':'false',
##                    'titleMap':title,
##                    'descriptionMap': '{"en_US":"none"}',
##                    'content': content,
##                    'ddmStructureKey':'BASIC-WEB-CONTENT',
##                    'ddmTemplateKey':'BASIC-WEB-CONTENT',
##                    'layoutUuid':'',
##                    'displayDateMonth':today.month-1,
##                    'displayDateDay':today.day,
##                    'displayDateYear':today.year,
##                    'displayDateHour':1,
##                    'displayDateMinute':1,
##                    'expirationDateMonth':expiredate.month-1,
##                    'expirationDateDay':expiredate.day,
##                    'expirationDateYear':expiredate.year,
##                    'expirationDateHour':1,
##                    'expirationDateMinute':1,
##                    'neverExpire':'false',
##                    'reviewDateMonth':0,
##                    'reviewDateDay':0,
##                    'reviewDateYear':0,
##                    'reviewDateHour':0,
##                    'reviewDateMinute':0,
##                    'neverReview':'true',
##                    'indexable':'true',
##                    'articleURL':item['url']}
## 
##         logger.info("Payload: %s",payload)
## 
##         r = requests.post(protocol + "://" + host + ":" + port + "/api/jsonws/journal.journalarticle/add-article", auth=(username, password), data=payload, headers=headers)
##         return item