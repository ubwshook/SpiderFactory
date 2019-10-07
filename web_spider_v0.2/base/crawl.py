import requests
import log


class Crawler:
    def __init__(self):
        self.encoding = 'utf-8'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        self.timeout = 5
        self.max_times = 10
        self.method = 'get'
        self.data = ''
        self.headers = {'User-Agent': self.user_agent}

    def set_headers(self, key, value):
        self.headers[key] = value

    def adpat_kwargs(self, **kwargs):
        if 'max_times' in kwargs.keys():
            self.max_times = kwargs['max_times']

        if 'method' in kwargs.keys():
            self.method = kwargs['method']

    def get_params(self, **kwargs):
        param_list = ['headers', 'cookies', 'timeout', 'data', 'proxies']
        paras = dict()
        paras['headers'] = self.headers
        paras['timeout'] = self.timeout

        for para_name in param_list:
            if para_name in kwargs.keys():
                paras[para_name] = kwargs[para_name]

        return paras

    def check_page(slef, page_text):
        return True

    def crawl(self, url, **kwargs):
        self.adpat_kwargs(**kwargs)
        times = 0
        while times < self.max_times:
            try:
                if 'session' in kwargs.keys():
                    session = kwargs['session']
                else:
                    session = requests.Session()

                paras = self.get_params(**kwargs)
                if self.method == 'post':
                    response = session.post(url=url, **paras)
                else:
                    response = session.get(url=url, **paras)
                if 'encoding' in kwargs.keys():
                    response.encoding = kwargs['encoding']
                else:
                    response.encoding = self.encoding

                if response.status_code == 200 and self.check_page(response.text):
                    return response, session
            except Exception as e:
                log.error("抓取出现错误: url={} error={}".format(url, str(e)))
                times += 1

        return None, None


0	149	20:45:03	SELECT itemId, title, startTime, endTime, acutionAddress,
 location, sellerNick,
 FROM taobao_sf.item_detail
 where bidstatus = 2	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'FROM taobao_sf.item_detail
 where bidstatus = 2' at line 3	0.000 sec



