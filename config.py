#!/usr/bin/env python3.5
# encoding: utf-8
"""
Created on 18-05-17

@author: Xsl
"""
import configparser
import os


# 获取config配置文件
def get_config(section, key):
    config = configparser.ConfigParser()
    # 其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
    path = os.path.join(os.path.dirname(__file__), 'settings.conf')
    config.read(path)
    return config.get(section, key)


logger_path = os.path.join(os.path.dirname(__file__), 'logging.conf')






