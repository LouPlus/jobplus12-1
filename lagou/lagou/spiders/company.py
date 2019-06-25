# -*- coding: utf-8 -*-
import scrapy

from lagou.items import LagouItem


class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/gongsi/']

    def parse(self, response):
        companys = response.css('li.company-item')
        for company in companys:
            item = LagouItem(
                logo=company.css('div.top').xpath('./p/a/img/@src').extract_first(),
                name=company.css('p.company-name').xpath('./a/text()').extract_first(),
                slogan=company.css('p.advantage::text').extract_first()
            )

            detail_url = company.css('div.top').xpath('./p/a/@href').extract_first()
            request = scrapy.Request(detail_url, self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        item['desc'] = response.css('span.company_content').xpath('./p/text()').extract_first()
        item['addr'] = response.css('div#container_right').xpath(
            './/div[@id="basic_container"]//li[4]/span/text()').extract_first()
        print(item)
        yield item
