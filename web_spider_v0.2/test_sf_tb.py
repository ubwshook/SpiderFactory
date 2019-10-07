from crawl import Crawler
import json
from common import get_regex
from tools.mysql_operator import MySqlOperator

url = 'https://sf.taobao.com/item_list.htm?city=&province=%D5%E3%BD%AD'
crawler = Crawler()
res, session = crawler.crawl(url=url, encoding='gbk')
raw_data = get_regex(r'<script id="sf-item-list-data" type="text/json">([\S\s]*?)</script>', res.text, 1)
jdata = json.loads(raw_data)

data_list = list()
for item in jdata['data']:
    item_info = {'id': item['id'], 'title': item['title']}
    data_list.append(item_info)


db = MySqlOperator(server='127.0.0.1', user_name='root', password='', dbname='taobao_sf')
db.bulk_insert('test_tb', data_list)
