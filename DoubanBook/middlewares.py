# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals




class DoubanbookSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#自定义的ip代理池配置		
import random  
import time
import scrapy  
from scrapy import log  

import sqlite3
import GetIP
import Config
import ProxiesDataBase
import Util
import schedule

# logger = logging.getLogger()  

class ProxyMiddleWare(object):  
    """docstring for ProxyMiddleWare"""



    def ip_spider(self):
        # 初始化数据库和数据表
        ProxiesDataBase.InitDB()
        # 刷新数据库，添加新数据
        Util.Refresh()

    # schedule.every(30).minutes.do(ip_spider)


    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        print("this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   


    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:
            ProxiesDataBase.InitDB.db_conn.execute('DELETE FROM IPPORT WHERE IP_PORT=proxy')
            proxy = self.get_random_proxy()  
            # print("this is response ip:"+proxy)
            # 对当前reque加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response  

    # def get_random_proxy(self):
    #     '''随机从文件中读取proxy'''
    #     while 1:
    #         with open('proxies.txt', 'r') as f:
    #             proxies = f.readlines()
    #         if proxies:
    #             break
    #         else:
    #             time.sleep(1)
    #     proxy = random.choice(proxies).strip()
    #     return proxy

    def get_random_proxy(self):
        # 初始化数据库和数据表
        ProxiesDataBase.InitDB()
        # 刷新数据库，添加新数据
        Util.Refresh()
        while len(GetIP.ip_list) < 10:
            self.ip_spider()
        proxy = Util.Get()
        return proxy