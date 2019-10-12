#! /usr/bin/python
# -*- coding:utf8 -*-

from credentials import MAIL_ADDRESS, PASSWORD


class Emailconfig:
    """邮件发送配置类"""
    def __init__(self, recipients, sender='', password=''):
        """
        :param recipients: list 收件人列表
        :param sender: string 发送人
        :param password: string 登录密码
        """
        self.recipients = recipients
        self.sender = MAIL_ADDRESS if sender == '' else sender
        self.password = PASSWORD if password == '' else password


class Logconfig:
    """日志文件解析配置类，如文件地址、解析方式、错误通知人等"""
    pattern = r'''\]\ (?P<ip>.*?)\ (.*)\ {.*?}\ \[(?P<datetime>.*?)\]\ (?P<request_method>POST|GET|DELETE|PUT|PATCH)\s
            (?P<request_uri>[^ ]*?)\ =>\ generated\ (?:.*?)\ in\ (?P<resp_msecs>\d+)\ msecs\s
            \(HTTP/[\d.]+\ (?P<resp_status>\d+)\)'''

    def __init__(self, filepath, emailconfig, pattern=''):
        self.filepath = filepath
        self.emailconfig = emailconfig

        if '' != pattern:
            self.pattern = pattern


files = [
    Logconfig(filepath='', emailconfig=Emailconfig(recipients=['kant@kantli.com'])),
    Logconfig(filepath='', emailconfig=Emailconfig(recipients=['kant@kantli.com'])),
]
