import time
from selenium import webdriver


class TouTiaoSpider():
    def __init__(self, need_number):
        self.url = 'https://www.toutiao.com/ch/news_hot/'
        self.browser = webdriver.Chrome()
        self.number = 1
        # 需要爬取几条数据
        self.need_number = need_number
        pass

    def save_data(self, data):
        """保存数据"""
        with open('./toutiao.txt', 'a', encoding='utf-8') as f:
            f.write(data + '\n')

    def get_response(self, list_element):
        """数据提取"""

        for li in list_element:
            try:
                if self.number > self.need_number:
                    break
                items = {}
                items["title"] = li.find_element_by_xpath('.//div[@class="title-box"]/a').text
                items["source"] = li.find_element_by_xpath('.//div[@class="y-left"]/a[2]').text
                items["comment"] = li.find_element_by_xpath('.//div[@class="y-left"]/a[3]').text
                items['time'] = li.find_element_by_xpath('.//div[@class="y-left"]/span[@class="lbtn"]').text
                items["url"] = li.find_element_by_xpath('.//div[@class="title-box"]/a').get_attribute('href')
                print("{}--第{}条数据--{}".format('*' * 40, self.number, '*' * 40))
                print(items)
                self.save_data(str(items))
                self.number += 1
            except Exception as e:
                pass

        pass

    def start_selenium(self):
        """启动selenium"""

        self.browser.get(self.url)
        while self.number < self.need_number:
            """爬取条件"""
            time.sleep(2)
            list_element = self.browser.find_elements_by_xpath('//div[@class="wcommonFeed"]/ul/li')
            # 数据提取
            self.get_response(list_element)
            # 进行两次滑动  不允许直接滑到底部
            self.browser.execute_script('window.scrollTo(0,200)')
            time.sleep(2)
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        print('数据已经到达:{}条----程序结束'.format(self.number - 1))
        pass

    def run(self):
        """启动爬虫"""

        self.start_selenium()
        time.sleep(4)
        self.browser.quit()
        pass


if __name__ == '__main__':
    user = TouTiaoSpider(100)
    # 需要爬取多少条数据  爬取100条数据
    user.run()
