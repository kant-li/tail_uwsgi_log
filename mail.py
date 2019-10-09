#! /usr/bin/python
# -*- coding: utf8 -*-

"""邮件通知"""

import smtplib
from email.mime.text import MIMEText

from config import Emailconfig


class Mail:
    """处理邮件构造等问题"""
    config = Emailconfig

    def __init__(self, title, msg, recipients):
        self.smtp = smtplib.SMTP_SSL(self.config.mail_host)

        self.recipients = recipients

        self.msg = MIMEText(msg, 'plain', 'utf-8')
        self.msg['subject'] = title
        self.msg['From'] = self.config.mail_addr
        self.msg['To'] = recipients

    def send(self):
        """发送邮件"""
        try:
            self.smtp.login(self.config.mail_addr, self.config.password)
            self.smtp.sendmail(self.config.mail_addr, self.recipients, self.msg.as_string())
            self.smtp.quit()
        except smtplib.SMTPException:
            pass
