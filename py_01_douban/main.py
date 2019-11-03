# -*- coding: UTF-8 -*-
# !/usr/bin/python
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import requests
import json
from pprint import pprint
import time


class DouBanSpider():
    """豆瓣热门页电影 爬虫"""

    def __init__(self):
        """初始化操作"""
        self.url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }
        self.pool = Pool(5)
        # 存放url的容器
        self.url_queue = Queue()
        # 爬取的数量
        self.number = 1

    def save_data(self, data):
        """保存数据"""
        with open('./douban.txt', 'a', encoding='utf-8') as f:
            f.write(data + '\n')

    def get_url(self, pages):
        """获取url"""
        for page in range(0, 20 * pages, 20):
            """要爬取几页数据"""
            url = self.url.format(page)
            self.url_queue.put(url)

    def execute_task(self):
        """获取数据"""
        url = self.url_queue.get()
        resp = requests.get(
            url=url,
            headers=self.headers
        )

        # 返回的数据是一个json数据, 转成字典格式
        result = json.loads(resp.text)
        # pprint(result) # pprint让控制台打印更好看
        result = result['subjects']

        for movie in result:
            items = {}
            items['title'] = movie['title']
            items['rate'] = movie['rate']
            items['url'] = movie['url']
            print(items)
            # 将数据保存
            self.save_data(str(items))
            self.number += 1
        self.url_queue.task_done()

    def execute_task_finished(self, result):
        """任务执行之后进行回调 result必须写"""
        self.pool.apply_async(self.execute_task, callback=self.execute_task_finished)

    def run(self, pages):
        """启动爬虫"""

        self.get_url(pages)
        for i in range(5):
            self.pool.apply_async(self.execute_task, callback=self.execute_task_finished)
        self.url_queue.join()


if __name__ == '__main__':
    start_time = time.time()
    user = DouBanSpider()
    # 要爬几页数据  就写多少页  下面是爬五页数据
    user.run(5)
    end_time = time.time()
    print('花费:{}'.format(end_time - start_time))
