# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    jobtitle = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    #pubdate = scrapy.Field()
    content = scrapy.Field()
    #pass

class GreifItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()

class WikipediaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class CityItem(scrapy.Item):
    url = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    intro = scrapy.Field()

class DoctorItem(scrapy.Item):
    url = scrapy.Field()
    lastname = scrapy.Field()
    initials = scrapy.Field()
    title = scrapy.Field()
    specialisation = scrapy.Field()
    experience = scrapy.Field()
    gender = scrapy.Field()
    city = scrapy.Field()
    rating = scrapy.Field()
    number_of_ratings = scrapy.Field()

class LegoItem(scrapy.Item):
    legoid = scrapy.Field()
    price = scrapy.Field()
    shop = scrapy.Field()
    url = scrapy.Field()