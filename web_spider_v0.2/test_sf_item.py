import json
import time
from urllib.parse import urlencode
from common import get_regex, field_mapping
from tb_tools import get_sign
from tools.mysql_operator import MySqlOperator
from crawl import Crawler

db = MySqlOperator(server='127.0.0.1', user_name='root', password='', dbname='taobao_sf')
rows = db.execute('SELECT distinct(itemId) FROM taobao_sf.sf_list_itemid').fetchall()
for row in rows:
    item_id = row[0]
    print(item_id)

    url = 'https://h5api.m.taobao.com/h5/mtop.taobao.govauctionmtopcommonservice.getfrontcategory/1.0/?jsv=2.4.5&appKey=12574478&t=1570096614606&api=mtop.taobao.govauctionmtopcommonservice.getfrontcategory'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36'
    }
    crawler = Crawler()
    res, session = crawler.crawl(url=url, headers=headers)
    cookies = res.cookies.get_dict()
    m_h5_tk = cookies['_m_h5_tk']
    app_key = '12574478'
    data = '{"itemId":"%s"}' % item_id
    sign, t = get_sign(m_h5_tk, app_key, data)
    params = {
        'jsv': '2.4.2',
        'appKey': app_key,
        't': t,
        'sign': sign,
        'api': 'mtop.taobao.GovauctionMTopDetailService.queryHttpsItemDetail',
        'v': '2.0',
        'ecode': '0',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp2',
        'data': data,
    }

    url = 'https://h5api.m.taobao.com/h5/mtop.taobao.govauctionmtopdetailservice.queryhttpsitemdetail/2.0/?' + urlencode(params)

    res, new_session = crawler.crawl(url=url, headers=headers, session=session)
    raw_data = get_regex(r'mtopjsonp2\(({[\s\S]*?})\)', res.text, 1)
    jdata = json.loads(raw_data)
    item = jdata['data']
    mapping_dict = {
        'itemId': 'itemId',
        'title': 'title',
        'startTime': 'startTime',
        'endTime': 'endTime',
        'auctionAddress': 'auctionAddress',
        'catId': 'catId',
        'consultPrice': 'consultPrice',
        'currentPriceLong': 'currentPriceLong',
        'bidStatus': 'bidStatus',
        'bidCycle': 'bidCycle',
        'location': 'location',
        'locationId': 'locationId',
        'sellerNick': 'sellerNick',
        'sellerId': 'sellerId',
        'serverTime': 'serverTime',
        'startPrice': 'startPrice',
        'incrementPrice': 'incrementPrice',
        'tradeType': 'tradeType',
        'foregiftPrice': 'foregiftPrice',
        'susong': 'susong',
    }

    item_info = dict()
    field_mapping(mapping_dict, item, item_info)
    print(item_info['title'])

    db.insert('item_detail', item_info)

