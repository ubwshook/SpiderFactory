'''------------------------------------------
文件名：WebSpider.py
作者： Shook
时间： 2018年9月23日
功能描述：定义爬虫基类：WebSpider，封装爬虫通用函数以及预留需要复写
的接口。
-------------------------------------------'''
import time
import requests
import log

# 爬虫主类
class WebSpider:
    # 初始化函数
    def __init__(self):
        self.taskId = int(time.time())

    # 设置请求信息的内容，除了URL外，其他参数都有默认值
    def setRequestInfo(self,
                   url,
                   userAgent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                   referer='',
                   cookie='',
                   isGzip=True,
                   maxTimes=10,
                   timeout=10,
                   encoding='utf8'):

        # 如果需要压缩就在请求头里添加gzip的字段
        if True == isGzip:
            headers = {
                'User-Agent': userAgent,
                'Cookie': cookie,
                'Referer': referer,
                'Accept-encoding': 'gzip'
            }
        else:
            headers = {
                'User-Agent': userAgent,
                'Cookie': cookie,
                'Referer': referer,
            }

        requestInfo = {
            'url': url,
            'headers': headers,
            'max_times': maxTimes,
            'timeout': timeout,
            'encoding': encoding,
            '_gzip': isGzip
        }

        return requestInfo

    # 请求页面，并解析出html文本
    def getHtml(self, requestInfo):
        url = requestInfo['url']
        headers = requestInfo['headers']
        encoding = requestInfo['encoding']
        maxtimes = requestInfo['max_times']
        timeout  = requestInfo['timeout']
        status = False
        times = 0
        #  一个页面最多请求maxtimes
        while times < maxtimes and not status:
            try:
                res = requests.get(url, headers=headers, timeout=timeout)
                res = res.content.decode(encoding)
                if '' == res:
                    times = times + 1
                    continue
                times = times + 1
            except Exception as e:
                log.error('请求 %s 出现错误：%s' % (url, e))
                continue
            status = True
        # 超过最大请求数，记录页面请求失败
        if times >= maxtimes:
            log.critical('%s 页面请求失败' % url)

        return res

    # 根据需要对页面进行解析，可以选择正则、xpath等等
    def htmlParse(self, html):
        return []

    # 如果要使用文件存储信息，覆写此函数
    def saveByFile(self, filename, data):
        return

    # 如果使用数据保存，覆写此函数
    def saveByDb(self, para, data):
        return

    # 存储信息函数，基类中默认数据库和文件方式存储
    def saveInfo(self, type, data, para):
        if type == 'f':
            try:
                self.saveByFile(para, data)
            except Exception as e:
                log.error('保存文件' + str(para) + '出现错误：' + str(e))
        elif type == 'db':
            try:
                self.saveByDb(para, data)
            except Exception as e:
                log.error('数据库' + str(para['dbName']) + '出现错误：' + str(e))
        else:
            print('错误的存储方式')
            log.error('错误的存储方式')

    # 启动爬虫主流程，如果需要更加复杂的控制逻辑，可以覆写这个函数
    def start(self):
        return []
