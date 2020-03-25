from base.crawl import Crawler
import json
import datetime
from tools.common import get_regex
import time
# coding=utf-8
import smtplib
from email.mime.text import MIMEText

def send_email(str):
    msg_from = 'skzhai@qq.com'  # 发送方邮箱
    passwd = 'fmcsvgnbazoxfffd'  # 填入发送方邮箱的授权码
    msg_to = 'skzhai@qq.com'  # 收件人邮箱

    subject = str  # 主题
    content = "这是我使用python smtplib及email模块发送的邮件"  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)   # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except Exception as e:
        print("发送失败" + str(e))
    finally:
        s.quit()



url = 'https://xueqiu.com/P/ZH2099343'
flag = True
flag2 = False
stock_name = ''
while True:
    crawler = Crawler()
    response, _ = crawler.crawl(url=url, timeout=5)
    data = get_regex(r'SNB.cubeInfo = ({[\s\S]*?});', response.text, 1)
    if flag:
        stock_name = json.loads(data)['view_rebalancing']['holdings'][0]['stock_name']
        weight = json.loads(data)['view_rebalancing']['holdings'][0]['weight']
        flag = False
    temp_name = json.loads(data)['view_rebalancing']['holdings'][0]['stock_name']
    print(temp_name, weight, datetime.datetime.now())
    if weight != 100 and not flag2:
        send_email(temp_name + '' + str(weight))
        flag2 = True
    if temp_name != stock_name:
        print("发送邮件")
        send_email(temp_name)
        stock_name = temp_name
    time.sleep(5)


# jdata = json.loads(response.text)
# info = jdata['rebalancing']['rebalancing_histories'][1]['stock_name']
# print(info, datetime.datetime.now())