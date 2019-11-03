# -*- coding: UTF-8 -*-
# !/usr/bin/python
import gevent.monkey

gevent.monkey.patch_all()
import time
from queue import Queue
from gevent.pool import Pool
import requests
import json
from urllib import request


class XiMaLaYaAllDataSpider():
    """喜马拉雅爬虫"""

    def __init__(self):
        """初始化"""
        self.basic_url = 'https://m.ximalaya.com/m-revision/common/album/queryAlbumTrackRecordsByPage?albumId=203355&page={}&pageSize=7'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }
        self.pool = Pool(3)
        self.url_queue = Queue()
        self.list_data = []

    def fun(self, blocknum, bs, size):
        """显示下载的进度"""
        percent = blocknum * bs / size
        percent = percent * 100
        int_data = int(percent)
        if int_data % 10 == 0:
            if int_data not in self.list_data:
                print("id:%s-----download: %d%%" % (blocknum, int_data))
                self.list_data.append(int_data)

    def get_url(self):
        """获取url列表"""

        for page in range(10):
            url = self.basic_url.format(page)
            # 将获取的url 存放进队列中
            self.url_queue.put(url)

    def exec_task(self):
        """定义执行任务代码"""
        # 从队列中获取url
        url = self.url_queue.get()
        resp = requests.get(url=url, headers=self.headers)
        # 提取数据  列表数据
        result = json.loads(resp.content)['data']["trackDetailInfos"]

        for sigle_data in result:
            """单个数据下的内容"""
            item = {}
            item["url"] = sigle_data["trackInfo"]["playPath"]
            item['name'] = sigle_data["trackInfo"]["title"][6:]
            print(item)
            # 下载音频
            down_url = request.urlretrieve(url=item['url'], filename='./down_file/' + item["name"] + '.mp3',
                                           reporthook=self.fun)
        print('*' * 50)
        time.sleep(2)
        self.url_queue.task_done()

    def exec_task_finished(self, result):
        """定义任务执行代码完成后回调"""
        self.pool.apply_async(self.exec_task, callback=self.exec_task_finished)

    def run(self):
        # 把所有url放入队列中
        self.get_url()

        #  让任务在线程池中的线程执行
        # callback 表示当任务执行完成后的回调函数
        # 默认情况下线程池中的线程都是守护线程
        for i in range(3):
            self.pool.apply_async(self.exec_task, callback=self.exec_task_finished)

        self.url_queue.join()


if __name__ == '__main__':
    start_time = time.time()
    user = XiMaLaYaAllDataSpider()
    user.run()
    end_time = time.time()
    print('花费多久：', end_time - start_time)
