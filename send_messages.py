import smtplib
from email.header import Header
from email.mime.text import MIMEText

import requests


def send_wechat_messages(messages):
    # server酱推送接口，申请地址：http://sc.ftqq.com/3.version
    url = 'https://sc.ftqq.com/{YOUR_KEY}.send'
    title = '机票通知'
    data = {'text': title, 'desp': messages}
    requests.post(url, data)


def send_email_messages(messages):
    #仅配置有注释的几行即可运行
    mail_host = ""  # 设置服务器
    mail_user = ""  # 用户名
    mail_pass = ""  # 口令
    sender = 'ctrip@ctrip.cn'
    receivers = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(messages, 'plain', 'utf-8')
    message['From'] = Header("携程", 'utf-8')
    message['To'] = Header("携程", 'utf-8')
    subject = '机票通知'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)  # 587 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        send_wechat_messages(e)
        print("send email failed %s" % e)
