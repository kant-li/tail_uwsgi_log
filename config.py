#! /usr/bin/python
# -*- coding:utf8 -*-


class Logconfig:
    pattern = r'''\]\ (?P<ip>.*?)\ (.*)\ {.*?}\ \[(?P<datetime>.*?)\]\ (?P<request_method>POST|GET|DELETE|PUT|PATCH)\s
            (?P<request_uri>[^ ]*?)\ =>\ generated\ (?:.*?)\ in\ (?P<resp_msecs>\d+)\ msecs\s
            \(HTTP/[\d.]+\ (?P<resp_status>\d+)\)'''
    email_recipients = ['kant@kantli.com']

    def __init__(self, filepath, pattern='', email_recipients=None):
        self.filepath = filepath
        if '' != pattern:
            self.pattern = pattern
        if email_recipients is not None and len(email_recipients) > 0:
            self.email_recipients = email_recipients


files = [
    Logconfig(filepath='uwsgi-0.log'),
    Logconfig(filepath='uwsgi-1.log'),
]
