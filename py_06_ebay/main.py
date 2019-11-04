# -*- coding: utf-8 -*-
import scrapy


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['ebay.com']

    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=huawei+&_sacat=9355&LH_TitleDesc=0&_sop=12&rt=nc&_pgn={}'

    def start_requests(self):
        """同时实现多个请求"""
        for page in range(1, 4):
            # 通过scrapy.Request将请求交给引擎
            yield scrapy.Request(
                self.url.format(page)
            )

    def parse(self, response):
        """解析函数"""
        li_element = response.xpath('//ul[@class="srp-results srp-list clearfix"]/li')
        for li in li_element:
            item = {}
            name = li.xpath('.//h3[@class="s-item__title"]/text()').extract_first()
            if not name:
                name = li.xpath('.//h3[@class="s-item__title s-item__title--has-tags"]/text()').extract_first()
            item['name'] = name
            item['price'] = li.xpath('.//div/span[@class="s-item__price"]/text()').extract_first()
            item['location'] = li.xpath(
                './/span[@class="s-item__location s-item__itemLocation"]/text()').extract_first()
            item['img'] = li.xpath('.//div[@class="s-item__image-wrapper"]/img//@src').extract_first()
            item['detail'] = li.xpath('.//div[@class="s-item__info clearfix"]/a/@href').extract_first()

            print(item)
            print('*' * 80)
            # 将数据交给管道
            yield item

        pass
