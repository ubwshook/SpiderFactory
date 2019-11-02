import scrapy
import json
import re
from tutorial.items import DemoItem
from tutorial.custom_settings import custom_setting_for_demo


class QuotesSpider(scrapy.Spider):
    name = "demo"
    custom_settings = custom_setting_for_demo

    def start_requests(self):
        urls = [
            'https://wqsou.jd.com/search/searchjson?datatype=1&page=3&pagesize=20&merge_sku=no&qp_disable=yes&key=ids%2C%2C1000004065&source=omz&g_login_type=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        raw_data = re.search(r'searchCB\(({[\s\S]*?})\)', str(response.text)).group(1)
        jdata = json.loads(raw_data.replace('\\', '\\\\'))
        goods = jdata['data']['searchm']['Paragraph']
        for good in goods:
            item = DemoItem()
            item['item_id'] = good['wareid']
            item['url'] = response.url
            yield item

