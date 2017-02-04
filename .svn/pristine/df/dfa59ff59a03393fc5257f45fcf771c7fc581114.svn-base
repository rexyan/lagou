#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import time
from Config import SQL_Helper


def sendmail(email_cont):
    # 第三方 SMTP 服务
    mail_host="219.216.128.9"  #设置服务器
    mail_user="yanrunsha13@nou.com.cn"    #用户名
    mail_pass="1530142917"   #口令

    sender = 'yanrunsha13@nou.com.cn'
    receivers = ['1572402228@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(email_cont, 'plain', 'utf-8')
    message['From'] = Header("数据抓取", 'utf-8')
    message['To'] =  Header("管理员", 'utf-8')
    subject = '拉勾数据抓取任务情况'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件",e)


