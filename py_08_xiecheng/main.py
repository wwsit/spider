# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy


class PlaySpider(scrapy.Spider):
    name = 'play'
    allowed_domains = ['ctrip.com']
    url = 'https://you.ctrip.com/sight/shenzhen26/s0-p{}.html#sightname'
    start_time = datetime.now()
    num_data = 1

    def start_requests(self):
        """实现多请求"""
        for page in range(1, 8):
            yield scrapy.Request(
                self.url.format(page)
            )

    def start_times(self, start_time):
        """开始时间"""

        # 使用日志记录起始运行时间
        self.save("开始运行时间：%s" % start_time)

    def end_times(self, start_time):
        """结束时间"""

        stop = datetime.now()
        self.save("结束运行时间：%s" % stop)
        self.save("耗时：%.2f" % (stop - start_time).total_seconds())

    def save(self, content):
        """保存内容"""

        print(type(content))
        print(content)
        with open('./xiecheng_log.txt', 'a', encoding='utf-8') as f:
            f.write(content + '\n')

    def parse(self, response):
        """解析函数"""

        # 记录开始时间
        self.start_times(self.start_time)

        list_element = response.xpath('//div[@class="list_wide_mod2"]/div')
        for li in list_element:
            # 提取想要的数据
            items = {}
            items['name'] = li.xpath('.//div[@class="rdetailbox"]//dt/a[@target="_blank"]/text()').extract_first()
            items['rank'] = li.xpath('.//div[@class="rdetailbox"]//dt/s/text()').extract_first()
            items['address'] = li.xpath(
                'normalize-space(.//div[@class="rdetailbox"]//dl//dd[@class="ellipsis"]/text())').extract_first()
            # 评分
            items['grade'] = li.xpath('.//ul[@class="r_comment"]//a/strong/text()').extract_first()
            # 评价
            items['evaluate'] = li.xpath('normalize-space(.//ul[@class="r_comment"]//a[@rel="nofollow"]/text())').extract_first()
            items['price'] = li.xpath('.//div[@class="rdetailbox"]//span[@class="price"]/text()').extract_first()
            detail_url = li.xpath('.//div[@class="rdetailbox"]//a/@href').extract_first()

            # 如果detail_url为None,跳过本次提取
            if not detail_url:
                continue
            items['detail_url'] = 'https://you.ctrip.com' + detail_url

            # 将数据交给引擎
            yield items
            self.save('第{}条数据---{}'.format(self.num_data, str(items)))
            self.num_data += 1

        # 记录结束时间
        self.end_times(self.start_time)
        pass
