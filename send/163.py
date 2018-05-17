#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-5-17
@title: '测试版'
@author: Xusl
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'xxxxxxxx@163.com'
receiver = 'xxxxxxxx@chyjr.com'
subject = 'python email test'
smtpserver = 'smtp.163.com'
username = 'xxxxxxxx@163.com'
password = 'xxxxxxxx'

msg = MIMEText('<html><h1>你好</h1></html>', 'html', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
