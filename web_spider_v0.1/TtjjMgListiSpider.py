'''------------------------------------------
文件名：TtjjMgListiSpider
作者： Shook
时间： 2018年10月21日
功能描述：基金经理列表抓取，来源：天天基金网
-------------------------------------------'''

import re
import WebSpider
import json
import datetime

# 创建一个爬虫对象
testSpider = WebSpider.WebSpider()

url = 'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=2000&pi=1&sc=abbname&st=asc'
# 请求页面
requestInfo = testSpider.setRequestInfo(url=url)
html = testSpider.getHtml(requestInfo)
# 为了进行json解析，把页面中一些不规范的地方进行修复，Json的属性名字要加上双引号
html = re.search(r'({[\s\S]+})', html).group(1).replace('data', '"data"')\
    .replace('record', '"record"').replace('pages', '"pages"').replace('curpage', '"curpage"')
# 加在json文本
a = json.loads(html)
mgData = a['data']
CONNECTION = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=fund;UID=shook;PWD=12345'
ctime = str(datetime.datetime.now())[0:10]
mgInfoList = list()
# 循环处理每一个经理的信息
for mg in mgData:
    print(mg)
    mgId = mg[0]
    mgName = mg[1]
    cyId = mg[2]
    cyName = mg[3]
    fundIdList = mg[4]
    fundNameList = mg[5]
    days = mg[6]
    bestScore = mg[7]
    bsetFundId = mg[8]
    bsetFundName = mg[9]
    scale = mg[10]
    mgInfo = {
        'mgId': mgId,
        'mgName': mgName,
        'cyId': cyId,
        'cyName': cyName,
        'fundIdList': fundIdList,
        'fundNameList': fundNameList,
        'days': days,
        'bestScore': bestScore,
        'bsetFundId': bsetFundId,
        'bsetFundName': bsetFundName,
        'scale': scale,
        'ctime': ctime
    }

    mgInfoList.append(mgInfo)

# 最后进行数据库批量保存
testSpider.saveByDb(CONNECTION, 'MgList', mgInfoList)

