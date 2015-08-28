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


class EastMoneySpider(CrawlSpider):
    name = "east"

    allowed_domains = [
        "stock.eastmoney.com"
    ]
    start_urls = [
        "http://stock.eastmoney.com/news/csbdt.html"
    ]

    #rules = [
    #    Rule(LinkExtractor(allow=("news/1614,[0-9]{17}")),callback='parse_east'),
    #]
    
    def parse(self,response):

        sites_even = Selector(response).css('div.listBox div.list ul li a')
        for site in sites_even:
            url = site.xpath('@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_east)
   
       #eastmoney
    def parse_east(self,response):
        
        sel = Selector(response)
        item = EastMoneyItem()
        content = ""
        item['link'] = get_base_url(response)
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['create_time'] = sel.css('div.Info span').xpath('text()').extract()[0]
        if len(sel.css('div.c_review').xpath('text()').extract()) > 0:
            item['info'] = sel.css('div.c_review').xpath('text()').extract()[0]
        else:
            item['info'] = ""
        list = sel.css('div.Body').xpath('//p').extract()
        for con in range(len(list)):
            if con != len(list)-1:
                content += list[con]

        item['content'] = content 
        item['source'] = 'eastmoney'
        item['source_type'] = 1 
        item['keyword'] = sel.xpath('//meta[2]/@content').extract()[0]
        item['description'] = sel.xpath('//meta[3]/@content').extract()[0]
        info('parsed ' + str(response)) 
        return item


    def _process_request(self, request):
        info('process ' + str(request))
        return request

        

"""       
       #eastmoney
    def parse_east(self,response):
        
        sel = Selector(response)
        item = EastMoneyItem()
        content = ""
        item['link'] = get_base_url(response)
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['create_time'] = sel.css('div.Info span').xpath('text()').extract()[0]
        if len(sel.css('div.c_review').xpath('text()').extract()) > 0:
            item['info'] = sel.css('div.c_review').xpath('text()').extract()[0]
        else:
            item['info'] = ""
        list = sel.css('div.Body').xpath('//p').extract()
        for con in range(len(list)):
            if con != len(list)-1:
                content += list[con]

        item['content'] = content 
        item['source'] = 'eastmoney'
        item['source_type'] = 1 
        item['keyword'] = sel.xpath('//meta[2]/@content').extract()[0]
        item['description'] = sel.xpath('//meta[3]/@content').extract()[0]
        info('parsed ' + str(response)) 
        return item
 
    # neeq 
    def parse_sec(self,response):   

        sel = Selector(response)
        item = TencentItem()
        item['companyName'] = sel.css('table.border1   tr:nth-child(2) > td:nth-child(3)').xpath("text()").extract()
        item['foundingTime'] = sel.css('table.border1   tr:nth-child(3) > td:nth-child(2)').xpath("text()").extract()
        item['registeredCapital'] = sel.css('table.border1   tr:nth-child(4) > td:nth-child(2)').xpath("text()").extract()
        item['manager'] = sel.css('table.border1   tr:nth-child(3) > td:nth-child(6)').xpath("text()").extract()
        info('parsed ' + str(response))
        return item

    def parse_item(self, response):
        items = []
        info('parsed ' + str(response))
        sel = Selector(response)
        base_url = get_base_url(response)
        sites_even = sel.css('div.qslb .qs_box')
        for site in sites_even:
            item = TencentItem()
            item['name'] = site.css('a').xpath("text()").extract()[2]
            item['url'] = urljoin_rfc(base_url, site.css('a').xpath("@href").extract()[0])
            info('parsed ' + str(response))
            yield scrapy.Request(item['url'], callback=self.parse_sec)             

"""

        