# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapyRootsItem(Item):
    # Primary
    title = Field()
    headers = Field()
    paragraphs = Field()
    links_text = Field()
    urls = Field()

    # Housekeeping
    url = Field()
    server = Field()

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass