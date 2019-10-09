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

import os
import re
import time


class Filereader:
    """读取文件"""
    def __init__(self, filename, tail_wait=1):
        """初始化日志阅读器，并检验是否为正确的日志文件
        :param filename: string 文件地址
        :param tail_wait: int default=1 跟踪文件变化的间隔时间
        """
        self.filename = filename
        self.tail_wait = tail_wait

        self._validate_filename()

    def read(self):
        """读取文件，逐行返回"""
        with open(self.filename) as f:
            for line in f:
                yield line

    def tail(self):
        """实现tail命令，跟踪文件动态"""
        with open(self.filename) as f:
            f.seek(0, 2)
            while True:
                current_position = f.tell()
                line = f.readline()
                if not line:
                    f.seek(current_position)
                    time.sleep(self.tail_wait)
                else:
                    yield line

    def _validate_filename(self):
        """确认文件存在、可读、并且不是文件夹"""
        if not os.access(self.filename, os.F_OK):
            raise FileNotFoundError('日志文件 ' + self.filename + ' 不存在')
        if not os.access(self.filename, os.R_OK):
            raise FileNotFoundError('日志文件 ' + self.filename + ' 不可读')
        if os.path.isdir(self.filename):
            raise FileNotFoundError(self.filename + ' 是文件夹而非日志文件')


class Logreader:
    """分析日志"""

    def __init__(self, filereader, re_pattern=r''):
        self.filereader = filereader
        self.pattern = re.compile(re_pattern, re.VERBOSE)

    def get_log_info(self):
        """获取日志信息"""
        lines = self.filereader.tail()
        while True:
            try:
                line = next(lines)
            except StopIteration:
                break
            else:
                result = self.re_log(line=line)
                if result is None:  # 无法解析，说明不是正常日志
                    pass
                elif result.get('resp_status', '') in []:  # 状态错误
                    pass

    def re_log(self, line):
        """用正则表达式解析log，如果满足表达式，返回解析结果，否则返回None"""
        result = self.pattern.search(line)
        if result:
            return result.groupdict()
        else:
            return result


# if __name__ == '__main__':
#     print('start' + ('*~' * 25))
#
#     from config import files
#     # reader = Filereader(filename='uwsgi-0.log')
#     # logreader = Logreader(reader, pattern)
#     # logreader.get_log_info()
#
#     print('end' + ('*~' * 25))
