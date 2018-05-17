#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-5-17
@title: '测试群发'
@author: Xusl
"""
import datetime
import config
import os
import logging

from send.send_email import send_email

logger = logging.getLogger(__name__)


def test():
    d_date = datetime.datetime.now()  # 获取当前时间
    current = datetime.datetime.strftime(d_date, '%Y-%m-%d')

    fz_team_path = config.get_config("db_param", "fz_team.path")
    file_path = os.path.join(fz_team_path, d_date.strftime('%Y%m%d'))

    file_list = []
    # os.walk()可以得到一个三元tupple(dirpath, dirnames, filenames)，
    # 其中第一个为起始路径，第二个为起始路径下的文件夹，第三个是起始路径下的文件。
    for parent, dir_names, file_names in os.walk(file_path):
        if parent == file_path:
            for file_name in file_names:
                file_list.append(file_name)

    # 获取需要发送的邮箱列表
    subject = '邮箱发送'
    report_list = []
    for file_name in file_list:
            report_list.append(file_name)
    attach_list = [
        {'name': 2,
         'to_email': 'xxxxxxxx@qq.com',  # 收件人
         'to_cc': '',  # 抄送人
         'parent': file_path,
         'subject': subject,
         'report': report_list,
         },
        {'name': 1,
         'to_email': 'zj123@chyjr.com',  # 收件人
         'to_cc': 'zj123@chyjr.com; zj456@chyjr.com;',   # 抄送人
         'parent': file_path,
         'subject': subject,
         'report': report_list,
         }
    ]

    # 获取发件人账号密码
    email_from = config.get_config("db_param", "email_from")
    email_user = config.get_config("db_param", "email_user")
    email_pwd = config.get_config("db_param", "email_pwd")
    content = """
            <meta>知几、您好！</meta>
            <p></p>
            &nbsp;&nbsp;<meta>今天是%s</meta>
            <meta>一个圣骑士成熟的标志是不再向盲人解释阳光。</meta>
        """ % (current,)
    content_type = 'html'
    success_num, false_num, result2 = send_email(email_from, email_user, email_pwd, attach_list, content, content_type)
    logger.debug(success_num, false_num, result2)
    print(success_num, false_num, result2)


if __name__ == '__main__':
    test()
