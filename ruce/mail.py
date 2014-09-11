#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2013,掌阅科技
All rights reserved.

File Name: mail.py
Author: WangLichao
Created on: 2014-06-06
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Mail(object):
    def __init__(self, smtp, user, pwd):
        self.smtp = smtp
        self.user = user
        self.pwd  = pwd
        self.isauth= True

    def parse_send(self, subject, content, plugin):
        return subject, content, plugin

    def send(self, subject, content, tolist, cclist=[], plugins =[], is_proxy=False):
        '''发送邮件
        Args:
            subject:标题
            content:内容
            tolist:收件人
            cclist:抄送人
            plugins:附件
            is_proxy:是否代理发送 True:代理发送:不需要登录;False:非代理发送：需要登录
        '''
        msg = MIMEMultipart()
        msg.set_charset('utf-8')
        msg['from'] = self.user
        msg['to'] = ','.join(tolist)
        if cclist:
            msg['cc'] = ','.join(cclist)
        msg['subject'] = subject
        msg.attach( MIMEText(content, 'html', 'utf-8'))
        for plugin in plugins:
            f = MIMEApplication(plugin['content'])
            f.add_header('content-disposition', 'attachment', filename=plugin['subject'])
            msg.attach(f)
        s = smtplib.SMTP(self.smtp)
        s.set_debuglevel(smtplib.SMTP.debuglevel)
        if self.isauth:
            s.docmd("EHLO %s" % self.smtp)
        try:
            s.ehlo()
            s.starttls()
        except smtplib.SMTPException,e:
            pass

        if not is_proxy:
            s.login(self.user, self.pwd)
        r = s.sendmail(self.user, tolist, msg.as_string())
        s.close()
        return r

if __name__== "__main__" :
    subject = '发送邮件测试'
    content = '<font color="#0000FF">测试</color>'
    #plugins = [{'subject':'附件1.txt','content':'内容1'},{'subject':'附件2.txt','content':'内容2'}]
    mail = Mail('smtp.zhangyue.com', 'wanglichao@zhangyue.com', 'zhangyue123')
    tolist = ['wanglichao@zhangyue.com']
    mail.send(subject, content, tolist)
    print 'send ok'
