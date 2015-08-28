import re
import json
import scrapy

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from news.items import *
from news.misc.log import *


class HexunSpider(CrawlSpider):
    name = "web"

    allowed_domains = [
        "stock.hexun.com"
    ]
    start_urls = [
        "http://stock.hexun.com/sanban/index.html"
    ]

    def parse(self,response):
        print get_base_url(response)
        sites_even = Selector(response).css('div.left ul.liBox li a')
        print sites_even
        for site in sites_even:
            url = site.xpath('@href').extract()[0]
            print url
            yield scrapy.Request(url, callback=self.parse_hexun)
   
    def parse_hexun(self,response):

        sel = Selector(response)
        item = EastMoneyItem()
        content = ""
        item['link'] = get_base_url(response)
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['create_time'] = sel.css('span#pubtime_baidu.gray::text').extract()[0]
        list = sel.css('div.art_context').xpath('//p').extract()
        for con in range(len(list)):
            if con != len(list)-1:
                content += list[con]
        item['info'] = ""
        item['content'] = content
        item['source'] = 'hexun'
        item['source_type'] = 2
        item['keyword'] = sel.xpath('//meta[2]/@content').extract()[0]
        item['description'] = sel.xpath('//meta[3]/@content').extract()[0]
        info('parsed 2' + str(response))
        return item
        
    def _process_request(self, request):
        info('process ' + str(request))
        return request




