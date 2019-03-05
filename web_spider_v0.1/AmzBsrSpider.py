'''------------------------------------------
文件名：AmzBsrSpider.py
作者： Shook
时间： 2018年9月23日
功能描述：亚马逊最佳销量榜品类采集爬虫，
以https://www.amazon.cn/gp/bestsellers为入口，
抓取左侧品类结构
---------------------------------------------
修改1：2018年11月10日
修改人： Shook
修改内容： 支持多线程抓取
-------------------------------------------'''
import WebSpider
import re
import log
import queue
from SpiderEnhance import SpiderThread
from SpiderEnhance import MultiProStarter
import time

# 定义AmzBsrSpider类，继承WebSpider
class AmzBsrSpider(WebSpider.WebSpider):
    # 初始化函数
    def __init__(self, threadCount, isProxy=False, **args):
        super(AmzBsrSpider, self).__init__(isProxy=isProxy, spiderName='Amazon category tree')
        # 建立一个队列用于存储不断生成URL信息
        self.urlQueue = queue.Queue()
        self.threadCount = threadCount

    # 抓取页面左侧的class="zg_selected"下的内容，采用正则表达式
    def regeContent(self, url, html):
        try:
            con = re.search('<span class="zg_selected">[\s\S]+</span>\s+</li>\s+<ul>([\s\S]+)</ul>\s+</li></ul>',
                            html).group(1)
            return con
        except Exception as e:
            log.error(url + str(e))
            return ''

    # 分解content中的每一个品类的信息
    def regexList(self, con):
        try:
            a2 = re.findall("<li><a href='(.*?)'>(.*?)</a></li>", con)
            return a2
        except Exception as e:
            log.error("抓取列表出现异常:" + str(e))
            return []

    # 页面解析函数，正则匹配页面，并且形成存储结构，刷新URL队列
    def htmlParse(self, html, urlInfo):
        result = list()
        url = urlInfo['url']
        level = urlInfo['level']
        # 正则匹配内容
        con = self.regeContent(url, html)
        # 正则匹配子树list列表
        conList = self.regexList(con)
        for i in conList:
            fatherUrl = url
            urlnew = i[0]
            tmp = urlnew.split('/')
            if 0 == level:
                cid = tmp[5]
            else:
                cid = tmp[6]
            name = i[1]
            # 以字典形式存储品类信息：父级URL，品类URL，品类名称，所处level和品类ID
            cateInfo = {'fatherUrl': fatherUrl,
                        'url': urlnew,
                        'cate_name': name,
                        'level': level + 1,
                        'cid': cid
                        }
            newUrlInfo = {
                'url': urlnew,
                'level': level + 1
            }
            result.append(cateInfo)
            # 新获取的URL放入队列
            self.urlQueue.put(newUrlInfo)

        return result

    # 文件形式存储
    def saveByFile(self, filename, data):
        dstFile = open(filename, 'a', encoding='utf-8')
        for single in data:
            dstFile.write(str(single))
            dstFile.write('\n')
        dstFile.close()
        return

    # 爬虫主流程，先把种子url放入队列，然后进行抓取，抓到的子类会补充到队列当中，
    # 只要队列不是空的，就一直继续抓取，直到所有品类都抓到
    def start(self):
        while not self.urlQueue.empty():
            urlInfo = self.urlQueue.get()
            requestInfo = self.setRequestInfo(url=urlInfo['url'])
            html = self.getHtml(requestInfo)
            data = self.htmlParse(html, urlInfo)
            self.saveInfo('f', data, 'bsr_cate_' + str(self.taskId) + '.txt')

        print("任务结束")
        log.critical("亚马逊品类信息抓取完毕")

    # 多线程启动函数，支持多线程后，调用此函数进行启动，原来的start将作为线程内启动函数
    def mthStart(self):
        url = 'https://www.amazon.cn/gp/bestsellers'
        log.critical("亚马逊品类信息爬虫启动")
        level = 0
        urlInfo = {
            'url': url,
            'level': level
        }
        self.urlQueue.put(urlInfo)
        thlist = list()
        for i in range(self.threadCount):
            th = SpiderThread(i, self.start)
            thlist.append(th)

        for i in range(self.threadCount):
            log.critical('线程 %s：开始运行(正常)', thlist[i].name)
            thlist[i].start()
            # 防止启动时队列空的情况
            time.sleep(5)

        for i in range(self.threadCount):
            log.critical('线程 %s：join', thlist[i].name)
            thlist[i].join()

if __name__=="__main__":
    flag = True  #是否使用多进程

    if not flag:
        # 实例化一个AmzBsrSpider，并且调用start函数将其启动。
        testSpider = AmzBsrSpider(3, isProxy=False)
        testSpider.mthStart()
    else:
        configList = list()

        configInfo = dict()
        configInfo['threadCount'] = 2
        configInfo['isProxy'] = False
        configInfo['crawlerClass'] = AmzBsrSpider
        configList.append(configInfo)

        configInfo = dict()
        configInfo['threadCount'] = 3
        configInfo['isProxy'] = False
        configInfo['crawlerClass'] = AmzBsrSpider
        configList.append(configInfo)

        starter = MultiProStarter()
        starter.start(configList, 2)




