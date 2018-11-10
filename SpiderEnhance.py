'''------------------------------------------
文件名：SpiderEnhance.py
作者： Shook
时间： 2018年11月10日
功能描述：爬虫增强模块，多线程，多进程，代理功能
-------------------------------------------'''
import threading
import log

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

