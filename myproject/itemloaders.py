import logging,re
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

REMOVE_ATTRIBUTES = [
    'lang','language','onmouseover','onmouseout','script','style','font',
    'dir','face','size','color','style','class','width','height','hspace',
    'border','valign','align','background','bgcolor','text','link','vlink',
    'alink','cellpadding','cellspacing','ng-non-bindable']


# You can do so much better here! 
def city(s):
    return s.split(",",1)[1]

def clean_me(s):
    return s.replace('Share', '').replace('share', '').strip()

def cleanser(s):
    return s.replace('\n', '').replace('\t', '').strip()

def clean_html(html):
    soup =  BeautifulSoup(html,'html.parser')
    for tag in soup.recursiveChildGenerator():
        try:
            logger.info("tag: " + str(tag))
            for k in list(tag.attrs.keys()):
                if k in REMOVE_ATTRIBUTES:
                    tag.attrs.pop(k, None)
        except AttributeError: 
            # 'NavigableString' object has no attribute 'attrs'
            pass

    return str(soup.prettify())

def get_lego_id(s):
    #val = s.split(':')[0]
    #return val.replace('<title>','')

    matches = re.findall("\d+", s)
    return matches[0]


class SearchDemoLoader(ItemLoader):

    default_output_processor = TakeFirst()

    jobtitle_in = MapCompose(lambda v: v.split())
    jobtitle_out = Join()

    department_in = MapCompose(clean_me, lambda v: v.split())
    department_out = Join()

    location_in = MapCompose(lambda v: v.split())
    location_out = Join()

    content_in = MapCompose(clean_html, lambda v: v.split())
    content_out = Join()

class BasicItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(remove_tags,lambda v: v.split())
    title_out = Join()

    content_in = MapCompose(clean_html, lambda v: v.split())
    content_out = Join()

    intro_in = MapCompose(cleanser, lambda v: v.split())
    intro_out = Join()

    subtitle_in = MapCompose(cleanser, lambda v: v.split())
    subtitle_out = Join()

class DoctorItemLoader(ItemLoader):
    city_in = MapCompose(city,lambda v: v.split())
    city_out = Join()

class LegoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    legoid_in = MapCompose(clean_html, get_lego_id, lambda v: v.split())
    legoid_out = Join()