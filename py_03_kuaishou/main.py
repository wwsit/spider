# -*- coding: UTF-8 -*-
# !/usr/bin/python

from gevent import monkey

import random
monkey.patch_all()
from  gevent.pool import Pool
from queue import Queue
import requests
from lxml import etree


class KuaiShouSpider():
    """快手爬虫"""

    def __init__(self, pages):
        """初始化"""

        self.url = 'https://live.kuaishou.com/cate/DQRM/?page={}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.pool = Pool(5)
        # 存放url的容器
        self.url_queue = Queue()
        self.pages = pages

    def get_proxy(self):
        """获取代理IP"""

        proxy = requests.get('http://127.0.0.1:6868/proxies/random').text
        proxies = {
            "http": proxy,
        }
        print(proxies)
        return proxies

    def get_url(self):
        """获取url"""

        for page in range(1, self.pages):
            url = self.url.format(page)
            self.url_queue.put(url)

    def save_data(self, items):
        """保存数据"""

        with open('./kuaishou.txt', 'a', encoding='utf-8') as f:
            f.write(items + '\n')

    def deal_response(self, list_element):
        """提取数据"""

        for li in list_element:
            """遍历列表内容"""
            items = {}
            items['name'] = li.xpath('normalize-space(.//p[@class="live-card-following-info-user"]/a/text())')
            items['room_name'] = li.xpath('normalize-space(.//div[@class="live-card-following-info"]//p[1]/a/text())')
            room_url = li.xpath('normalize-space(.//div[@class="live-card live-card"]/a/@href)')
            items['room_url'] = 'https://live.kuaishou.com' + room_url
            items['game_name'] = li.xpath(
                'normalize-space(.//div[@class="live-card-following-info"]//p[1]//span/text())')
            print(items)
            self.save_data(str(items))

    def execute_task(self):
        """执行函数"""

        # 从容器中取出url
        url = self.url_queue.get()
        # resp = requests.get(url=url, headers=self.headers)
        resp = requests.get(url=url, headers=self.headers, proxies=self.get_proxy())

        eroot = etree.HTML(resp.text)
        list_element = eroot.xpath('.//div[@class="live-card-list-container"]/ul/li')
        print(len(list_element))

        self.deal_response(list_element)
        self.url_queue.task_done()
        pass

    def execute_task_finished(self, result):
        """任务完成之后 回调函数"""
        self.pool.apply_async(self.execute_task, callback=self.execute_task_finished)

    def run(self):
        """启动程序"""
        self.get_url()
        for i in range(5):
            self.pool.apply_async(self.execute_task, callback=self.execute_task_finished)
        self.url_queue.join()
        pass


if __name__ == '__main__':
    user = KuaiShouSpider(4)
    # 需要爬取几页数据
    user.run()
