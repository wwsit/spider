# -*- coding: UTF-8 -*-
# !/usr/bin/python
import scrapy
from datetime import datetime
from amazon_scrapy.spiders.logs.log import logger


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['amazon.cn']

    # 用来拼接的url
    basic_url = 'https://www.amazon.cn/s?bbn=665002051&rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A664978051%2Cn%3A665002051%2Cp_89%3A{}&dc&fst=as%3Aoff&qid=1568986091&rnid=125596071&ref=sr_in_-2_p_89_0'
    # 全部分类的url
    start_urls = [
        "https://www.amazon.cn/gp/search/other/ref=amb_link_13?ie=UTF8&n=665002051&pickerToList=brandtextbin&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-left-7&pf_rd_r=2PEQE5EQ16VQEN3G8PZC&pf_rd_r=2PEQE5EQ16VQEN3G8PZC&pf_rd_t=101&pf_rd_p=b8021ffc-61f8-44ee-8d7f-c48db7a7c960&pf_rd_p=b8021ffc-61f8-44ee-8d7f-c48db7a7c960&pf_rd_i=664978051"]
    start_time = datetime.now()
    data_num = 1

    def start_times(self, start_time):
        """开始时间"""
        logger.info("开始运行时间：%s" % start_time)  # 使用日志记录起始运行时间
        self.save("开始运行时间：%s" % start_time)

    #
    def end_times(self, start_time):
        """结束时间"""
        stop = datetime.now()  # 结束时间
        logger.info("结束运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start_time).total_seconds())  # 使用日志记录运行耗时
        self.save("结束运行时间：%s" % stop)
        self.save("耗时：%.2f" % (stop - start_time).total_seconds())

    #
    def save(self, content):
        """保存内容"""
        print(type(content))
        print(content)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.write(content + '\n')

    def parse(self, response):
        """1.手机列表SPU"""
        self.start_times(self.start_time)
        list_data = response.xpath('//div[@id="ref_125596071"]/ul/li')

        # 所有手机列表
        for sigle_data in list_data:
            item = {}

            item['name'] = sigle_data.xpath('.//span[@class="refinementLink"]/text()').extract_first()
            # 获取初步的url
            initial_url = sigle_data.xpath('.//a[@class="a-link-normal"]/@href').extract_first()
            # 对url进行拼接
            result = initial_url[initial_url.rfind('%3A') + 3:]
            # 获取最终url
            new_url = self.basic_url.format(result)
            item['url'] = new_url
            # 发送请求
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_detail_list
            )

        pass

    def parse_detail_list(self, response):
        """sku商品页面"""
        print(response.url)
        self.save('当前爬的url-----{}'.format(response.url))

        sku_list = response.xpath('//div[@class="s-result-list s-search-results sg-row"]/div')
        for sigle_sku in sku_list:
            # 获取每个sku商品信息
            item = {}
            item['name'] = sigle_sku.xpath(
                './/span[@class="a-size-medium a-color-base a-text-normal"]/text()').extract_first()
            item['price'] = sigle_sku.xpath('.//span[@class="a-price-whole"]/text()').extract_first()
            detail_url = sigle_sku.xpath('.//div[@class="a-section a-spacing-none"]//a/@href').extract_first()
            print(detail_url)
            item['detail_url'] = 'https://www.amazon.cn' + detail_url

            self.save('{}个数据----{}'.format(self.data_num, item))
            print(item)

            # 将数据交给引擎
            yield item
            self.data_num += 1

        print('*' * 60)
        self.save('*' * 60)

        # 下一页
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            # 拼接url
            new_url = 'https://www.amazon.cn' + next_page
            # print(new_url)

            # 发送请求
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_detail_list
            )
        self.end_times(self.start_time)
