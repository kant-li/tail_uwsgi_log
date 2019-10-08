#! usr/bin/python
# -*- coding:utf8 -*-
"""
读取文件的脚本

参考日志行：
[pid: 6814|app: 0|req: 1990/15726]
110.90.29.160 () {60 vars in 2074 bytes}
[Mon Sep  9 10:17:57 2019] POST /api/order/order_detail => generated 2558 bytes in 83 msecs
(HTTP/1.1 200) 7 headers in 403 bytes (2 switches on core 1)
"""

import re


class Filereader:
    """读取文件"""
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        """读取文件，逐行返回"""
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    yield line
        except FileNotFoundError:
            raise


class Logreader:
    """分析日志"""

    def __init__(self, filereader, re_pattern=r''):
        self.filereader = filereader
        self.pattern = re.compile(re_pattern, re.VERBOSE)

    def get_log_info(self):
        """获取日志信息"""
        lines = self.filereader.read()
        # while True:
        for i in range(10):
            try:
                line = next(lines)
            except StopIteration:
                break
            else:
                print(self.re_log(line=line))

    def re_log(self, line):
        """用正则表达式解析log，如果满足表达式，返回解析结果，否则返回None"""
        result = self.pattern.search(line)
        if result:
            return result.groupdict()
        else:
            return result


if __name__ == '__main__':
    print('start' + ('*~' * 25))

    pattern = r'''\]\ (?P<ip>.*?)\ (.*)\ {.*?}\ \[(?P<datetime>.*?)\]\ (?P<request_method>POST|GET|DELETE|PUT|PATCH)\s
        (?P<request_uri>[^ ]*?)\ =>\ generated\ (?:.*?)\ in\ (?P<resp_msecs>\d+)\ msecs\s
        \(HTTP/[\d.]+\ (?P<resp_status>\d+)\)'''

    reader = Filereader(filename='uwsgi-0.log')
    logreader = Logreader(reader, pattern)
    logreader.get_log_info()

    print('end' + ('*~' * 25))
