import time
import json
import threading
from base import log
from crawl import Crawler
PROXY_LIST = list()


class ProxyThread(threading.Thread):
    def __init__(self, interval, name, num, flag=True):
        self.interval = interval
        self.flag = flag
        self.num = num
        threading.Thread.__init__(self, name=name)

    def run(self):
        start_mark = False
        crawler = Crawler()
        while self.flag:
            try:
                url = 'http://hw.venndata.cn/proxy?num={num}'.format(num=self.num)

                response, _ = crawler.crawl(url=url)
                html = response.text
                if html:
                    data = json.loads(html)['data']
                    proxy_list = data.split('|')
                    if len(proxy_list) > 500:
                        old_len = len(PROXY_LIST)
                        PROXY_LIST.extend(proxy_list)
                        PROXY_LIST[0:old_len] = []
                    if not start_mark:
                        log.critical("代理启动成功！获取代理%s" % len(proxy_list))
                        start_mark = True
            except Exception as e:
                log.error('生成 Proxy Failed'+str(e))
            time.sleep(self.interval)

        log.info('代理关闭')
        return

