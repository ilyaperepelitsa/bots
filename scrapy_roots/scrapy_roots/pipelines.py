# -*- coding: utf-8 -*-
import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.sql import select

from scrapy.exceptions import DropItem

def inst_to_dict(inst, delete_id = True):
    dat = {}
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    if delete_id:
        dat.pop("num")
    return dat


engine_webpage = create_engine("sqlite:////root/quant/bots/scrapy_roots/scrapy_roots/webpage.db", echo = False)
Base_webpage = declarative_base()

class Webpage(Base_webpage):
    __tablename__ = "crawled"
    num = Column(Integer, primary_key = True)
    title = Column(String)
    headers = Column(String)
    paragraphs = Column(String)
    links_text = Column(String)
    time = Column(String)
    url = Column(String)
    domain = Column(String)


    def __repr__(self):
        return "<Base_webpage(title='%s', headers='%s', paragraphs='%s', links_text='%s', time='%s', url='%s', domain='%s')>"\
        %(self.title, self.headers, self.paragraphs, self.links_text, self.time, self.url, self.domain)


Base_webpage.metadata.create_all(engine_webpage)


Session_webpage = sessionmaker(bind = engine_webpage)
session_webpage = Session_webpage()


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapyRootsPipeline(object):
#     def process_item(self, item, spider):
#         return item

class ProcessItem(object):
    def process_item(self, item, spider):

        item["title"] = [re.sub( '\t+', '', title).strip() for title in item["title"]]
        item["title"] = [re.sub( '\s+', ' ', title).strip() for title in item["title"]]
        item["title"] = [title for title in item["title"] if title != ""]
        item["title"] = ' '.join(item["title"])

        item["headers"] = [re.sub( '\t+', '', header).strip() for header in item["headers"]]
        item["headers"] = [re.sub( '\s+', ' ', header).strip() for header in item["headers"]]
        item["headers"] = [header for header in item["headers"] if header != ""]
        item["headers"] = ' '.join(item["headers"])

        item["paragraphs"] = [re.sub( '\t+', '', paragraph).strip() for paragraph in item["paragraphs"]]
        item["paragraphs"] = [re.sub( '\s+', ' ', paragraph).strip() for paragraph in item["paragraphs"]]
        item["paragraphs"] = [paragraph for paragraph in item["paragraphs"] if paragraph != ""]
        item["paragraphs"] = ' '.join(item["paragraphs"])

        item["links_text"] = [re.sub( '\t+', '', link_text).strip() for link_text in item["links_text"]]
        item["links_text"] = [re.sub( '\s+', ' ', link_text).strip() for link_text in item["links_text"]]
        item["links_text"] = [link_text for link_text in item["links_text"] if link_text != ""]
        item["links_text"] = ' '.join(item["links_text"])

        item["time"] = item["time"][0]

        item["url"] = item["url"][0]

        # item["domain"] = item["url"][0].replace("http://","").replace("https://","").replace("www.", "").replace("ww2.", "").strip()
        item["domain"] = item["url"].replace("http://","").replace("https://","").replace("www.", "").replace("ww2.", "").strip().split("/")[0]


        if item['paragraphs'] == "":
            raise DropItem("Missing paragraph in %s" % item)
        else:
            return item


class RecordWebpage(object):

    def process_item(self, item, spider):

        webpage_entry = {"title" : item["title"],
                        "headers" : item["headers"],
                        "paragraphs" : item["paragraphs"],
                        "links_text" : item["links_text"],
                        "time" : item["time"],
                        "url" : item["url"],
                        "domain" : item["domain"]}

        if len([inst_to_dict(w) for w in session_webpage.query(Webpage).filter(Webpage.url == item["url"])]) == 0:
            session_webpage.add(Webpage(**webpage_entry))
            session_webpage.commit()
            return item
        else:
            raise DropItem("Link already exists %s" % item)

#
# from pandas import DataFrame
# DataFrame
# newdf = [inst_to_dict(w) for w in session_webpage.query(Webpage)]
# DataFrame(newdf)
