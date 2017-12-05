# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 书名
    images = scrapy.Field()  # 图片
    author = scrapy.Field()  # 作者
    press = scrapy.Field()  # 出版社
    date = scrapy.Field()  # 出版日期
    page = scrapy.Field()  # 页数
    price = scrapy.Field()  # 价格
    ISBN = scrapy.Field()  # ISBN号
    score = scrapy.Field()  # 豆瓣评分
    author_profile = scrapy.Field()  # 作者简介
    content_description = scrapy.Field()  # 内容简介
    link = scrapy.Field()  # 详情页链接
