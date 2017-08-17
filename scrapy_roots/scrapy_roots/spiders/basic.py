# -*- coding: utf-8 -*-
 # !/usr/bin/python
import scrapy
from scrapy_roots.items import ScrapyRootsItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import re
import datetime
import socket

class BasicSpider(scrapy.Spider):
    name = "basic"
    # allowed_domains = ["web"]
    start_urls = ['http://brandmark.io/font-generator/']

    def parse(self, response):
        # scrapy crawl basic -o "ftp://user:pass@ftp.scrapybook.com/items.json "
        l = ItemLoader(item = ScrapyRootsItem(), response = response)
        l.add_xpath("title", '//title/text()')
        l.add_xpath("headers", '//h1/text()')
        # l.add_xpath("paragraphs", '//p/text()')
        l.add_xpath("paragraphs", '//p/text()', MapCompose(str.strip), Join())
        l.add_xpath("links_text", '//a/text()')
        l.add_xpath("urls", '//a/@href')

        l.add_value('url', response.url)
        # l.add_value('start_url', )
        # l.add_value('project', self.settings.get('BOT_NAME'))
        # l.add_value('spider', self.name)
        # l.add_value('server', socket.gethostname())
        # l.add_value('date', datetime.datetime.now())

        result = l.load_item()

        return result

        # print(result["paragraphs"])

        # item = ScrapyRootsItem()
        # item["title"] = response.xpath('//title/text()').extract()
        # item["headers"] = response.xpath('//h1/text()').extract()
        # item["paragraphs"] = response.xpath('//p/text()').extract()
        # item["links_text"] = response.xpath('//a/text()').extract()
        # return item


        # self.log("title: %s" % response.xpath('//title/text()').extract())
        # self.log("headers: %s" % response.xpath('//h1/text()').extract())
        # self.log("paragraphs: %s" % response.xpath('//p/text()').extract())
        # self.log("links: %s" % response.xpath('//a/text()').extract())
