# -*- coding: UTF-8 -*-
# !/usr/bin/python
import scrapy
from datetime import datetime
from amazon_scrapy.spiders.logs.log import logger


class BookSpider(scrapy.Spider):
    """最畅销的新图书"""

    name = 'book'
    allowed_domains = ['amazon.com']
    basic_url = 'https://www.amazon.com/gp/new-releases/books/283155/ref=zg_bsnr_pg_2?ie=UTF8&pg={}'
    start_time = datetime.now()
    num = 1

    def start_requests(self):
        """实现多个请求"""

        for page in range(1, 3):
            # 把请求提交给引擎
            yield scrapy.Request(
                url=self.basic_url.format(page)
            )

    def start_times(self, start_time):
        """开始时间"""

        logger.info("开始运行时间：%s" % start_time)
        # 使用日志记录起始运行时间
        self.save("开始运行时间：%s" % start_time)

    def end_times(self, start_time):
        """结束时间"""

        stop = datetime.now()
        logger.info("结束运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start_time).total_seconds())  # 使用日志记录运行耗时
        self.save("结束运行时间：%s" % stop)
        self.save("耗时：%.2f" % (stop - start_time).total_seconds())


    def save(self, content):
        """保存内容"""

        print(type(content))
        print(content)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.write(content + '\n')

    def parse(self, response):
        """数据提取"""

        self.start_times(self.start_time)
        li_element = response.xpath('//ol[@id="zg-ordered-list"]//li')

        for li in li_element:
            """获得单个元素"""

            item = {}
            item['rank'] = li.xpath('.//span[@class="zg-badge-text"]/text()').extract_first()
            item['name'] = li.xpath(
                'normalize-space(.//div[@class="p13n-sc-truncate p13n-sc-line-clamp-1"]/text())').extract_first()
            item['price'] = li.xpath('.//span[@class="p13n-sc-price"]/text()').extract_first()
            detail_url = li.xpath('.//span[@class="a-list-item"]//a/@href').extract_first()
            item['detail_url'] = "https://www.amazon.com" + detail_url
            item['Release_time'] = li.xpath(
                './/div[@class="a-row"]/span[@class="zg-release-date"]/text()').extract_first()

            print(item)
            yield item
            self.save('第{}条数据---{}'.format(self.num,str(item)))
            self.num += 1
        self.end_times(self.start_time)
