#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-5-17
@title: '邮件发送'
@author: Xusl
"""
import os
import logging

import smtplib


from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

logger = logging.getLogger(__name__)


# 把一个标头的用户名编码成utf-8格式的，如果不编码原标头中文用户名，用户名将无法被邮件解码
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(email_from, email_user, email_pwd, attach_list, content, content_type):
    """
    邮件发送
    :param email_from: 发件人邮箱
    :param email_user: 发件人
    :param email_pwd: 发件人邮箱密码
    :param attach_list: 收件人列表
    :param content: 正文
    :param content_type: 正文类型
    :return:
    """
    result = []
    success_num = 0
    fail_num = 0
    # 发送单个分公司邮件
    for attach in attach_list:
        logger.info(attach)
        name = attach['name']
        msg = MIMEMultipart()
        to_email = attach['to_email']
        msg['From'] = _format_addr(email_from)
        email_list = to_email.split(';')
        cc = attach['to_cc']
        subject = attach['subject']
        to_list = []
        for i_to in email_list:
            # 去除首尾空格
            i_to = i_to.strip()
            if i_to:
                to_list.append(_format_addr('<%s>' % i_to))
        # 把抄送人邮件列表转化为字符串, 在每个邮件地址中间加入,
        msg['To'] = ','.join(to_list)
        cc_list = []
        for i_cc in cc.split(';'):
            # 去除首尾空格
            i_cc = i_cc.strip()
            if i_cc:
                cc_list.append(_format_addr('<%s>' % i_cc))
        msg['Cc'] = ','.join(cc_list)
        msg['Subject'] = Header(subject, 'utf-8').encode()

        content1 = MIMEText(content, content_type, 'utf-8')
        # class email.mime.text.MIMEText(_text, _subtype, _charset)：MIME文本对象
        msg.attach(content1)
        # message.attch(payload) 将给定的附件或信息,添加到已有的有效附件或信息中,
        # 在调用之前必须是None或者List,调用后payload将变成信息对象的列表
        report_file_path = attach['parent']
        for report_file in attach['report']:
            # 将目录名和文件的基名拼接成一个完整的路径
            path = os.path.join(report_file_path, report_file)
            # 返回path最后的文件名
            basename = os.path.basename(path)
            fp = open(path, 'rb')
            att = MIMEApplication(fp.read())
            att["Content-Type"] = 'application/octet-stream'
            # add_header(_name, _value, **_params) 扩展标头设置 _name:要添加的标头字段  _value:标头的内容
            # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名.比如：*.gif;*.txt;
            att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', basename))
            encoders.encode_base64(att)
            # 将att的内容编码为base64格式
            msg.attach(att)
        # 发送邮件
        server = None
        print(email_user, email_pwd, email_list)
        try:
            # 定义发送邮件
            # server = smtplib.SMTP_SSL('smtp.qq.com', )
            # server.ehlo()
            server = smtplib.SMTP()
            server.connect('smtp.163.com')

            # 登陆到smtp服务器
            server.login(email_user, email_pwd)
            #  SMTP.sendmail(from_addr, to_addrs, msg[mail_options, rcpt_options]) ：发送邮件。
            #  msg是字符串，表示邮件。发送邮件的时候，要注意msg的格式。这个格式就是smtp协议中定义的格式。
            # 我们知道邮件一般由标题，发信人，收件人，邮件内容，附件等构成，
            # 第二个参数，接受邮箱为一个列表，表示可以设置多个接受邮箱
            # as_string()是MIMEMessage对象的一个方法，表示把MIMETest对象变成str
            server.sendmail(email_user, email_list + cc.split(";"), msg.as_string())
        except Exception as e:
            logger.info('%s发送失败:连接服务器或发送邮件出现异常' % name)
            logger.info(str(e))
            result.append({
                'name': name,
                'to_email': to_email,
                'to_cc': cc,
                'status': '0',
                'msg': str(e),
            })
            fail_num += 1
        else:
            result.append({
                'name': name,
                'to_email': to_email,
                'to_cc': cc,
                'status': '2',
                'msg': None,
            })
            success_num += 1
            logger.debug('%s发送成功' % name)
        finally:
            try:
                if server:
                    # 断开与smtp服务器的连接
                    server.quit()
            except Exception as e:
                logging.info(str(e))
    return success_num, fail_num, result

