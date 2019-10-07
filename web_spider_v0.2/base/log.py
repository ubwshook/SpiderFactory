import os
import logging
import datetime
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\log'

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
date = datetime.datetime.now().strftime("%Y%m%d")

formatter_file = logging.Formatter('%(asctime)s %(process)d %(thread)d %(filename)s %(lineno)d %(levelname)s: %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')

#文件日志
Rthandler = RotatingFileHandler(BASE_DIR+'\\crawl_%s.log' % (date),
                                maxBytes=5*1024*1024, backupCount=1)
Rthandler.setLevel(logging.INFO)
Rthandler.setFormatter(formatter_file)

console = logging.StreamHandler()
console.setLevel(logging.CRITICAL)
console.setFormatter(formatter_file)

log = logging.getLogger('CRAWL')
log.setLevel("INFO")
log.addHandler(Rthandler) #其他模块使用的接口
log.addHandler(console)

debug = log.debug
info = log.info
warning = log.warning
error = log.error
critical = log.critical

