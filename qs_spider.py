import requests
from lxml import etree
import json


class QiushiSpider(object):

    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}

    def get_url_list(self):
        url_list = [self.temp_url.format(i) for i in range(1, 14)]
        return url_list

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):

        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@id='content-left']/div")
        content_list = []
        for div in div_list:
            item = {}
            item["author"] = div.xpath(".//div[@class='author clearfix']//h2/text()")[0].strip()
            item["content"] = div.xpath(".//div[@class='content']/span[1]/text()")
            item["content"] = [i.strip() for i in item["content"]]
            # for i in item["content"]:
            content_list.append(item)
        return content_list

    def save_content_list(self, content_list):
        with open("qiushi.txt", "a") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")
        print("保存成功")

    def run(self):
        url_list = self.get_url_list()

        for url in url_list:
            html_str = self.parse_url(url)
            content_list = self.get_content_list(html_str)
            self.save_content_list(content_list)


if __name__ == '__main__':
    qiushi = QiushiSpider()
    qiushi.run()