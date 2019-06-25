# -*- coding: utf-8 -*-
import scrapy

from lagou.items import JobItem


class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = ['https://www.lagou.com/zhaopin/?filterOption=3']

    def parse(self, response):
        jobs = response.css('li.con_list_item')
        print(jobs)
        for job in jobs:
            yield JobItem(
                name=job.xpath('.//a[@class="position_link"]/h3/text()').extract_first(),
                addr=job.xpath('.//a[@class="position_link"]/span/em/text()').extract_first()
            )
