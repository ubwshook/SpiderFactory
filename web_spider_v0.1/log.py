import logging
from logging.handlers import RotatingFileHandler
'''日志记录模块，记录所有操作的日志'''

#文件日志
Rthandler = RotatingFileHandler('crawl.log', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.ERROR)
formatter_file = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s')
Rthandler.setFormatter(formatter_file)

#窗口日志
console = logging.StreamHandler()
console.setLevel(logging.CRITICAL )
formatter_console = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s')
console.setFormatter(formatter_console)

#将文件和窗口句柄 赋给Logger
#logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger('CRAWL')
log.setLevel(logging.DEBUG)
log.addHandler(Rthandler) #其他模块使用的接口
log.addHandler(console)

#重命名
debug = log.debug
info = log.info
warning = log.warning
error = log.error
critical = log.critical



