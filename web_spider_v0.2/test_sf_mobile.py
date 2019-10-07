import json
import time
from urllib.parse import urlencode
from common import get_regex, field_mapping
from tb_tools import get_sign
from tools.mysql_operator import MySqlOperator
from crawl import Crawler
from sf_cate import cate_list

db = MySqlOperator(server='127.0.0.1', user_name='root', password='', dbname='taobao_sf')
city = '三门峡'
for cate_info in cate_list:
    cate_id = cate_info['id']
    cate_name = cate_info['name']
    print(cate_name)
    page = 1
    while True:
        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.govauctionmtopcommonservice.getfrontcategory/1.0/?jsv=2.4.5&appKey=12574478&t=1570096614606&api=mtop.taobao.govauctionmtopcommonservice.getfrontcategory'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36'
        }
        crawler = Crawler()
        res, session = crawler.crawl(url=url, headers=headers)
        cookies = res.cookies.get_dict()
        m_h5_tk = cookies['_m_h5_tk']
        app_key = '12574478'
        data = '{"city":"%s","pageNo":%s,"pageSize":99,"orderId":"0","categoryId":"%s"}' % (city, str(page), cate_id)
        sign, t = get_sign(m_h5_tk, app_key, data)
        params = {
            'jsv': '2.4.5',
            'appKey': app_key,
            't': t,
            'sign': sign,
            'api': 'mtop.taobao.govauction.sfsearchlist',
            'v': '1.0',
            'H5Request': 'true',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp14',
            'data': data,
        }

        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.govauction.sfsearchlist/1.0/?' + urlencode(params)

        res, new_session = crawler.crawl(url=url, headers=headers, session=session)
        raw_data = get_regex(r'mtopjsonp14\(({[\s\S]*?})\)', res.text, 1)
        jdata = json.loads(raw_data)
        items = jdata['data']['itemList']
        mapping_dict = {
            'itemId': 'itemId',
            'title': 'title',
            'bidCount': 'bidCount',
            'bidStatus': 'bidStatus',
            'currentPrice': 'currentPrice',
            'delayTimes': 'delayTimes',
            'endTime': 'endTime',
            'orgLoan': 'orgLoan',
            'sellerNick': 'sellerNick',
            'serverTime': 'serverTime',
            'startTime': 'startTime',
            'status': 'status'
        }

        data_list = list()
        for item in items:
            item_info = dict()
            field_mapping(mapping_dict, item, item_info)
            item_info['cate_name'] = cate_name
            item_info['cate_id'] = cate_id
            item_info['city'] = city
            data_list.append(item_info)

        db.bulk_insert('sf_list_itemid', data_list)

        print(page, len(items))
        totalCount = jdata['data']['totalCount']
        total_page = int(totalCount) // 99 + 1
        page += 1
        if page > total_page:
            break
        time.sleep(5)


