# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from ZhiHu.items import ZhihuuserItem


class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']

    # "寺主人"url_token
    start_user = 'sizhuren'

    # 个人信息页url
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # "关注的人"列表url
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # "粉丝"列表url
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    followers_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        """初始请求"""
        # 请求个人信息
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        # 请求"关注的人"列表
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0), callback=self.parse_follows)
        # 请求"粉丝"列表
        yield Request(self.follows_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),callback=self.parse_followers)


    def parse_user(self,response):
        """解析个人信息"""
        # 转化成json对象
        results = json.loads(response.text)
        # 声明item对象
        item = ZhihuuserItem()
        # 依次获取每一个field
        for field in item.fields:
            if field in results.keys():
                # 赋值
                item[field] = results.get(field)
        yield item

        # 请求每一个人的"关注的人"列表,"粉丝"列表
        yield Request(self.follows_url.format(user=results.get('url_token'),include=self.follows_query,limit=20,offset=0),callback=self.parse_follows)
        yield Request(self.followers_url.format(user=results.get('url_token'),include=self.followers_query,limit=20,offset=0),callback=self.parse_followers)


    def parse_follows(self,response):
        """解析'关注的人'列表"""
        results = json.loads(response.text)
        if 'data' in results.keys():
            # 依次获取每一个关注人的url_token, 进行解析
            for result in results.get('data'):
                # 请求解析
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),callback=self.parse_user)
        # 翻页判断，False表示需要翻页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            # 下一页url
            next_page = results.get('paging').get('next')
            yield Request(next_page,callback=self.parse_follows)


    def parse_followers(self,response):
        """解析'粉丝'列表"""
        results = json.loads(response.text)
        if 'data' in results.keys():
            # 依次获取每一个粉丝的url_token
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),callback=self.parse_user)
        # 翻页判断，False表示需要翻页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            # 下一页url
            next_page = results.get('paging').get('next')
            yield Request(next_page,callback=self.parse_followers)









