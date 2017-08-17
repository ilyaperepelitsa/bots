# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field

from scrapy_roots.items import ScrapyRootsItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.http import Request

import re
import datetime
import socket

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.sql import select

def inst_to_dict(inst, delete_id = True):
    dat = {}
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    if delete_id:
        dat.pop("num")
    return dat



engine_crawled = create_engine("sqlite:///crawled.db", echo = False)
Base_crawled = declarative_base()

class Crawled(Base_crawled):
    __tablename__ = "crawled"
    num = Column(Integer, primary_key = True)
    crawled_link = Column(String)



    def __repr__(self):
        return "<Base_crawled(crawled_link='%s')>"\
        %(self.crawled_link)


Base_crawled.metadata.create_all(engine_crawled)


Session_crawled = sessionmaker(bind = engine_crawled)
session_crawled = Session_crawled()

[inst_to_dict(w) for w in session_crawled.query(Crawled)]

class DomainLinks(Item):
    links = Field()

class EasySpider(CrawlSpider):
    name = 'easy'
    # allowed_domains = ['web']
    start_urls = ['http://liguriafoods.com/where-to-buy/']

    rules = (
    # Rule(LinkExtractor(restrict_xpaths="//*[not(contains(text(),'@'))]")),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse', follow=True),
    )



    # def parse_start_url(self, response):
    #     self.parse_links(response)
    #
    #
    # def parse_links(self, response):



    def parse(self, response):

        crawledLinks = []

        l = ItemLoader(item = ScrapyRootsItem(), response = response)
        l.add_xpath("title", '//title/text()')
        l.add_xpath("headers", '//h1/text()')
        # l.add_xpath("paragraphs", '//p/text()')
        l.add_xpath("paragraphs", '//p/text()', Join())
        l.add_xpath("links_text", '//a/text()')
        l.add_xpath("urls", '//a/@href')

        l.add_value('url', response.url)
        # l.add_value('start_url', )
        # l.add_value('project', self.settings.get('BOT_NAME'))
        # l.add_value('spider', self.name)
        # l.add_value('server', socket.gethostname())
        # l.add_value('date', datetime.datetime.now())

        # print(l.load_item())

        # yield result
        # print(domain)
        # print(links)
        # print("\n\n")


        # item = DomainLinks()
        # item['links'] = []
        # domain = response.url.replace("http://","").replace("https://","").strip("www.").strip("ww2.").split("/")[0]
        # links = LinkExtractor(allow=(),deny = ()).extract_links(response)
        # links = [link for link in links if domain in link.url]
        # links = [link for link in links if link.url.replace("http://","").replace("https://","").startswith(domain) and link.url != response.url]
        # print(links)
        # # Filter duplicates and append to
        # for link in links:
        #     if link.url not in item['links']:
        #         item['links'].append(link.url)
        #
        # print(item)
        # return item["links"]



        # item = []
        # domain = response.url.replace("http://","").replace("https://","").strip("www.").strip("ww2.").split("/")[0]
        # links = LinkExtractor(allow=(),deny = ()).extract_links(response)
        # links = [link for link in links if domain in link.url]
        # links = [link for link in links if link.url.replace("http://","").replace("https://","").startswith(domain) and link.url != response.url]
        # print(links)
        # # Filter duplicates and append to
        # for link in links:
        #     if link.url not in item:
        #         item.append(link.url)
        #
        # print(item)
        # return item
        #
        #
        pew = ScrapyRootsItem()
        pew["title"] = response.xpath('//title/text()').extract()



        item = []
        domain = response.url.replace("http://","").replace("https://","").replace("www.", "").replace("ww2.", "").split("/")[0]
        links = LinkExtractor(allow=(),deny = (), unique = True).extract_links(response)
        links = [link for link in links if domain in link.url]
        # print(links)
        links = [link for link in links if link.url.replace("http://","").replace("https://","").replace("www.", "").replace("ww2.", "").startswith(domain) and link.url != response.url]
        # print(links)
        # Filter duplicates and append to
        for link in links:
            if link.url not in item:
                item.append(link.url)

        # for i in item:
        #     print("\n")
        #     print(i)
        #     print("\n")
        # print(len([inst_to_dict(w) for w in session_crawled.query(Crawled).filter(Crawled.crawled_link == link)]))



        # print(item)
        for link in item:
            if len([inst_to_dict(w) for w in session_crawled.query(Crawled).filter(Crawled.crawled_link == link)]) == 0:
                crawled_entry = {"crawled_link" : link}
                session_crawled.add(Crawled(**crawled_entry))
                session_crawled.commit()
            # print("\n")
            # print(link)
            # print("\n")

                req = scrapy.Request(link, callback = self.parse)
                req.meta["dont_redirect"] = True
                req.meta["handle_httpstatus_list"] = [301, 302, 303]
                yield req




        # print(item)
        # print(crawledLinks)
        # return(pew)
        # print(pew["title"])
