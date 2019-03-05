'''------------------------------------------
文件名：TtjjFundListSpider
作者： Shook
时间： 2018年10月21日
功能描述：基金列表抓取，来源：天天基金网
-------------------------------------------'''

import time
import re
import WebSpider

# 创建一个爬虫对象
testSpider = WebSpider.WebSpider()

# 基金类型字典，拼接URL的使用
typeList = {
    '股票型': 'gp',
    '债券型': 'zq',
    '混合型': 'hh',
    '指数型': 'zs',
    '保本型': 'bb',
    'QDII': 'qdii',
    'LOF': 'lof',
    'FOF': 'fof'
}

# 任务ID，用采集时的时间戳
taskId = int(str(time.time())[0:10])
for type in typeList:
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=%s&rs=&gs=0&sc=zzf&st=desc&sd=2017-10-19&ed=2018-10-19&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.5211739473795021' %typeList[type]
    requestInfo = testSpider.setRequestInfo(url=url)

    html = testSpider.getHtml(requestInfo)
    rankData = re.search(r'(\[.*\])',
                    html).group(1)

    fundList = re.findall(r'"(.*?)"', html)
    print(type + ":" + str(len(fundList)))
    fundInfoList = list()
    CONNECTION = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=fund;UID=shook;PWD=12345'

    for fund in fundList:
        fund = fund.split(',')
        code = fund[0]  # 基金代码
        name = fund[1]  # 基金名称
        name_en = fund[2]  # 基金拼音缩写
        fundInfo = {
            'code': int(code),
            'name': name,
            'name_en': name_en,
            'type': type,
            'taskId': taskId
        }

        fundInfoList.append(fundInfo)

    # 数据库方式保存
    testSpider.saveByDb(CONNECTION, 'fundlist', fundInfoList)





