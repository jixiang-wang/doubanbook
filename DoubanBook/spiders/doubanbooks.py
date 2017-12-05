# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DoubanbookItem
import re
import os
import urllib.request
from scrapy.http import HtmlResponse, Request
from scrapy.conf import settings  # 从settings文件中导入Cookie，这里也可以from scrapy.conf import settings.COOKIE
import random
import string


class BookspiderSpider(CrawlSpider):
    name = 'bookSpider'
    allowed_domains = ['book.douban.com']
    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    #获取随机的cookies
    cookies = "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    start_urls = ['https://book.douban.com/tag/爬虫?start=0&type=T']
    rules = (
        # 列表页url
        Rule(LinkExtractor(allow=(r"tag/爬虫?start=\d+&type=T")),follow = True),
        # 详情页url
        Rule(LinkExtractor(allow=(r"subject/\d+/$")), callback="parse_item",  follow = True)
    )
    #将获取到的cookie传递给每一个url链接的ruquest
    def request_question(self, request):
        return Request(request.url, meta={'cookiejar': 1}, callback=self.parse_item)

    #获取详情页具体的图书信息
    def parse_item(self, response):

        if response.status == 200:
            item = DoubanbookItem()
            # 图书名
            item["name"] = response.xpath("//div[@id='wrapper']/h1/span/text()").extract()[0].strip()
            # 图书的图片
            src = response.xpath("//div[@id='mainpic']/a/img/@src").extract()[0].strip()
            file_name = "%s.jpg" % (item["name"])  # 图书名
            file_path = os.path.join("E:\\spider\\pictures\\douban_book\\spider", file_name)  # 拼接这个图片的路径
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(src, file_path)  # 接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径
            item["images"] = file_path
            #作者
            if len(response.xpath("//div[@id='info']/span[1]/a/text()").extract()) > 0:
                authors = response.xpath("//div[@id='info']/span[1]/a/text()").extract()
                item["author"] = ",".join(author.strip() for author in authors).strip()
            else:
                authors = response.xpath("//div[@id='info']/a[1]/text()").extract()
                item["author"] = ",".join(author.strip() for author in authors).strip()
            #出版社
            try:
                item["press"] = response.xpath("//div[@id='info']").re(r'出版社:</span> (.+)<br>\n')[0].strip()
            except:
                item["press"] = "无"
            #出版年
            try:
                item["date"] = response.xpath("//div[@id='info']").re(r'出版年:</span> (.+)<br>\n')[0].strip()
            except:
                item["date"] = "无"
            #页数
            try:
                page_str = response.xpath("//div[@id='info']").re(r'页数:</span> (.+)<br>\n')[0].strip()
                item["page"] = int(re.findall(r'\d+', page_str)[0])
            except:
                item["page"] = "无"
            #定价
            try:
                item["price"] = response.xpath("//div[@id='info']").re(r'定价:</span> (.+)<br>\n')[0].strip()
            except:
                item["price"] = "无"
            #ISBN
            try:
                item["ISBN"] = response.xpath("//div[@id='info']").re(r'ISBN:</span> (.+)<br>\n')[0].strip()
            except:
                item["ISBN"] = "无"
            # 豆瓣评分

            if len(response.xpath("//div[@class='rating_self clearfix']/strong/text()").extract()[0].strip()) > 0:
                item["score"] = float(response.xpath("//div[@class='rating_self clearfix']/strong/text()").extract()[0].strip())
            else:
                item["score"] = "评价人数不足"

            # 内容简介
            try:
                if len(response.xpath('//span[@class="all hidden"]/div/div[@class="intro"]/p')) > 0:
                    contents = response.xpath('//span[@class="all hidden"]/div/div[@class="intro"]/p/text()').extract()
                    item["content_description"] = "\n".join(content.strip() for content in contents)
                elif len(response.xpath('//div[@id="link-report"]/div/div[@class="intro"]/p')) > 0:
                    contents = response.xpath('//div[@id="link-report"]/div/div[@class="intro"]/p/text()').extract()
                    item["content_description"] = "\n".join(content.strip() for content in contents)
                else:
                    item["content_description"] = "无"
            except:
                item["content_description"] = "无"
            # 作者简介


            try:
                profiles_tag = response.xpath('//div[@class="related_info"]/div[@class="indent"]').extract()[1]

                profiles = profiles_tag.xpath('/div[@class="intro"]/p/text()').extract()
                print(profiles)
                if len(profiles[0]) > 0:
                    item["author_profile"] = "\n".join(profile.strip() for profile in profiles)

                else:
                    item["author_profile"] = "无"
            except:
                item["author_profile"] = "无"

            # 详情页链接
            item["link"] = response.url

            return item
