# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZhihuuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 引入了Item和Field就不用再scrapy.
    # 用户id
    id = Field()
    # 用户头像
    avatar_url = Field()
    # 关注数
    follower_count = Field()
    # 性别
    gender = Field()
    # 描述
    headline = Field()
    # 昵称
    name = Field()
    # url_token
    url_token = Field()

