# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MinispiderItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    domain = scrapy.Field()
    indexing_timestamp = scrapy.Field()
    lang_detected = scrapy.Field()
    images = scrapy.Field()
    videos = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    date_published = scrapy.Field()
    date_modified = scrapy.Field()
    article = scrapy.Field()
    tags = scrapy.Field()
    comments = scrapy.Field()
