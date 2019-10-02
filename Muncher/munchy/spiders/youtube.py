# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

#FILE = open('items.csv', 'a')

ID_LSTRIP = '/watch?v='

class YoutubeSpider(CrawlSpider):
    
    name = 'youtube'
    allowed_domains = ['youtube.com']
    start_urls = ['https://www.youtube.com/watch?v=bXcSLI58-h8']

    def parse(self, response):
        item = {}

        upnext_link = response.xpath(
            '//*[@id="watch7-sidebar-modules"]/div[1]/div/div[2]'
            '/ul/li/div[1]/a/@href').get()
        recommendations = response.xpath('//*[@id="watch7-sidebar-modules"]/div[2]/div/ul/*/div[1]/a/@href').getall()
        item['id'] = response.url[response.url.index(ID_LSTRIP)+len(ID_LSTRIP):]
        item['title'] = response.xpath('/html/head/meta[@name="title"]/@content').get()
        raw_count = response.xpath('//*[@id="watch7-views-info"]/div[@class="watch-view-count"]/text()').get()
        item['count'] = int(raw_count.rstrip(' views').replace(',', '')) if raw_count else None
        item['duration'] = None
        item['uploaddate'] = response.xpath('//*[@id="watch-uploader-info"]/strong/text()').get()
##        item['tags'] = response.xpath('/html/head/meta[@property="og:video:tag"]/@content').getall()
        item['category'] = response.xpath('//*[@id="watch-description-extras"]/ul/li[1]/ul/li/a/text()').get()
        item['upnext'] = upnext_link.lstrip(ID_LSTRIP) if upnext_link else None
        item['recommends'] = [u.lstrip(ID_LSTRIP) for u in recommendations]

        yield item
        yield scrapy.Request(response.urljoin(upnext_link))
        for next_page_url in recommendations:
            yield scrapy.Request(response.urljoin(next_page_url))
