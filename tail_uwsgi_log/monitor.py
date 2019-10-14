#! /usr/bin/python
# -*- coding:utf8 -*-

"""监控脚本"""

import asyncio
import argparse
import configparser

from tail_uwsgi_log.reader import Filereader, Logreader, Mailsender
from tail_uwsgi_log.config import Emailconfig, Logconfig


async def monitor(configs):
    """监控日志文件"""
    # 每个文件都创建对应任务
    tasks = []
    for file in configs:
        logreader = Logreader(re_pattern=file.pattern)
        mailsender = Mailsender(emailconfig=file.emailconfig)
        filereader = Filereader(filename=file.filepath, logreader=logreader, mailsender=mailsender,
                                wait_time=file.wait_time)
        tasks.append(filereader.tail())
    # 执行任务
    await asyncio.gather(*tasks)


def tail_uwsgi_log():
    """Script to parse configs and execute log tail"""
    parser = argparse.ArgumentParser(prog='tail_uwsgi_log', description='Tail uwsgi logs')
    parser.add_argument('-c', '--config', type=str, help='Config file path')

    configs = parse_config(parser.parse_args().config)

    for config in configs:
        print(config)
        pass


def parse_config(filepath):
    """从配置文件中读取信息"""
    conf = configparser.ConfigParser()
    conf.read(filepath)

    configs = []
    for section in conf.sections():
        if section.startswith('log'):
            config = {
                'filepath': conf.get(section, 'filepath') if conf.has_option(section, 'filepath') else '',
                'wait_time': conf.getfloat(section, 'wait_time') if conf.has_option(section, 'wait_time') else 1,
                'pattern': conf.get(section, 'pattern') if conf.has_option(section, 'pattern') else '',
            }
            config.update(parse_mail_config(conf, section))
            configs.append(config)

    return configs


def parse_mail_config(conf, section):
    """读取邮件配置信息"""
    mail_info = {
        'mail_host': '',
        'mail_port': '',
        'mail_sender': '',
        'mail_password': '',
        'mail_recipients': '',
    }
    if conf.has_section('mail'):
        for k in mail_info.keys():
            if conf.has_option('mail', k):
                mail_info[k] = conf.get('mail', 'mail_host')

    for k in mail_info.keys():
        if conf.has_option(section, k):
            mail_info[k] = conf.get(section, k)

    try:
        mail_info['mail_port'] = int(mail_info['mail_port'])
    except ValueError:
        mail_info['mail_port'] = 465

    return mail_info


if __name__ == '__main__':
    asyncio.run(monitor())
