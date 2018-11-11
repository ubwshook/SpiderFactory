'''------------------------------------------
文件名：SpiderEnhance.py
作者： Shook
时间： 2018年11月10日
功能描述：爬虫增强模块，多线程，多进程，代理功能
-------------------------------------------'''
import threading
import log
import urllib
import json
import time
import gvalue
import WebSpider

# 多线程模块，将爬虫启动函数传递给线程即可
class SpiderThread(threading.Thread):
    def __init__(self, threadId, func):
        tname = 'th' + str(threadId)
        threading.Thread.__init__(self, name=tname)
        self.threadId = threadId
        self.begin = func

    def run(self):
        log.critical('线程%s 启动' % self.threadId)
        self.begin()


# 代理线程，用于获取代理列表
class proxyThread(threading.Thread):
    def __init__(self, interval, pack):
        self.interval = interval
        self.pack = pack
        tname = 'proxy'
        threading.Thread.__init__(self, name=tname)

    def run(self):

        index = 0

        while True:
            try:
                # 这里的代理池在网上购买的
                url = 'http://api.66daili.cn/API/GetCommonProxy/?orderid=2891740301801427631&num=1000&token=XXX&format=json&line_separator=win&protocol=http&anonymous=elite,anonymous,transparent&area_exclude=%E4%B8%AD%E5%9B%BD&proxytype=https&speed=fast,quick,slow#api'
                html = urllib.request.urlopen(url, timeout=60).read().decode('utf-8')
                if html != None:
                    proxyList = json.loads(html)['proxies']
                    WebSpider.proxyList = proxyList
                    print('库存' + str(len(proxyList)) + '调代理' + self.pack)

                flag = gvalue.get_value('proxySwitch')
                print(flag)
                if False == flag:
                    print('关闭代理')
                    break;

            except Exception as e:
                log.critical('生成 Proxy Failed' + str(e))
            time.sleep(self.interval)

