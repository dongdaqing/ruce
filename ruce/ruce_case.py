#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2013,掌阅科技
All rights reserved.

File Name: ruce_case.py
Author: WangLichao
Created on: 2014-03-17
'''
#sys
import sys
import os
import time
import unittest
import logging
import re
from collections import defaultdict
#third
import requests
import yaml
import json
#self
import logger
import utils
from utils import Config
from utils import tree

class ConfError(Exception):
    '''错误异常封装
    '''
    def __init__(self,errmsg):
        self.errmsg=errmsg

    def __str__(self):
        return "error occured ,msg is :%s" % self.errmsg

class RuceCase(unittest.TestCase):
    '''用于执行http请求的单元测试
    Attributes:
        uri: http请求的uri
        url: http请求完整url
        retry: http重试次数
        timeout: 超时时间设置
        headers: http请求头
        method: http请求方法
        good_case: 好的测试用例
        bad_case: 坏的测试用例
        result_list: 返回结果列表
        bad_results: 坏的测试用例结果
        good_results: 好的测试用例结果
        config: 配置信息
    '''
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.requests = requests
        self.conf_file = 'ruce.conf.yml'
        self.uri = None
        self.url = None
        #default retry times
        self.retry = 1
        #http timeout
        self.timeout = None
        #http headers
        self.headers = None
        #http proxies
        self.proxies = None
        #default requests method
        self.method = 'GET'
        #default case type can only be dict or str
        self.good_case = None
        self.bad_case = None
        #save requests results
        self.result_list = defaultdict(list)
        self.good_results = None
        self.bad_results = None
        #init config
        self.config = None
        files = os.listdir('.')
        if self.conf_file not in files:
            raise ConfError('ruce.conf.yml file is not init')
        with open(self.conf_file) as conf_file:
            self.config = Config(yaml.load(conf_file))
            #init log
            #if 'log_conf' in self.config:
            #    logger.init_logger(self.config.log_conf)
        #self.logger = logging.getLogger('ruce')

    def ruce_log(self, msg, level='info'):
        log, handler = logger.init_logger(self.config.log_conf)
        if level == 'info':
            log.info(msg)
        elif level == 'warning':
            log.warning(msg)
        elif level == 'error':
            log.error(msg)
        log.removeHandler(handler)

    def test_good(self):
        if not hasattr(self, 'verify_good_case'):
            return
        good_cases = []
        if hasattr(self, 'add_good_case'):
            good_cases = self.add_good_case()
        else:
            good_cases.append(self.good_case)
        self.verify_cases(good_cases, kind='good')
        #add subclass verify
        self.verify_good_case()

    def test_bad(self):
        if not hasattr(self, 'verify_bad_case'):
            return
        bad_cases = []
        if hasattr(self, 'add_bad_case'):
            bad_cases = self.add_bad_case()
        else:
            bad_cases.append(self.bad_case)
        self.verify_cases(bad_cases, kind='bad')
        #add subclass verify
        self.verify_bad_case()

    def verify_cases(self, cases, kind='good'):
        '''返回结果验证
        Args:
            cases: 设置的测试用例，list类型
            kind: 测试用例类别，为good 还是 bad
        '''
        assert kind in ('good', 'bad'), 'kind can only be good or bad'
        env_name = self.config.env['use_env']
        print_url = self.config.screen_print.get('http_url', '0')
        print_code = self.config.screen_print.get('http_code', '0')
        print_body = self.config.screen_print.get('http_body', '0')
        for case in cases:
            url = self.create_url(env_name, case)
            if int(print_url):
                print '[   %s %s ]' % (self.method.upper(), url)
            response = None
            self.proxies = self.config.http.get('proxies', None)
            for i in xrange(self.retry):
                self.ruce_log('[ run {0} times={1} ]'.format(self.uri, i+1))
                try:
                    if self.method.upper() == 'GET':
                        timeout = self.timeout or self.config.http['get']['timeout']
                        response = self.requests.get(url, timeout=timeout, headers=self.headers, proxies=self.proxies)
                        if response.status_code == 200:
                            break
                    else:
                        timeout = self.timeout or self.config.http['post']['timeout']
                        if isinstance(case, (dict, str)):
                            response = self.requests.post(url, data=case, timeout=timeout, headers=self.headers, proxies=self.proxies)
                            if response:
                                break
                        else:
                            self.ruce_log('[ case type error,support type is dict and str ]', level='error')
                except Exception,e:
                    self.ruce_log('[ request error,{}]'.format(e), level='error')
                    continue
            self.ruce_log('[ {0} {1} ]'.format(self.method.upper(), url))
            self.ruce_log('[ code {} ]'.format(response.status_code))
            if int(print_code):
                print '[   code {} ]'.format(response.status_code)
            body_info = ''
            if len(response.text) > 300:
                if int(print_body):
                    print '[   body {0} ... {1} ]'.format(response.content[0:100], response.content[-100:])
                self.ruce_log('[ body {0} ... {1} ]'.format(response.content[0:100], response.content[-100:]))
            else:
                if int(print_body):
                    print '[   body {} ]'.format(response.content)
                self.ruce_log('[ body {} ]'.format(response.content))
            #assert int(response.status_code) >= 400, 'http status code is bigger than 400'
            res = {}
            res['code'] = response.status_code
            try:
                if response.json():
                    res['json_data'] = response.json()
                    res['body'] = response.content
                else:
                    res['body'] = response.content
                self.result_list[kind].append(res)
            except Exception,e:
                #如果返回值不能被json解析会抛异常
                self.ruce_log('[ response can not json decode,url=%s ]' % url)
                res['body'] = response.content
                self.result_list[kind].append(res)

        #如果结果唯一则保存结果对象，否则保存结果list
        if len(self.result_list['good']) == 1:
            self.good_results = self.result_list['good'][0]
        else:
            self.good_results = self.result_list['good']
        if len(self.result_list['bad']) == 1:
            self.bad_results = self.result_list['bad'][0]
        else:
            self.bad_results = self.result_list['bad']

    def create_url(self, env_name, case=None):
        '''生成对应环境请求的url
        Args:
            env:环境
            case:请求的case
        Return:
            返回拼接完整的url
        '''
        if self.url:
            return self.url
        url = None
        url_params = None
        if case and self.method.upper() == 'GET':
            if isinstance(case, dict):
                url_params = '&'.join([str(k)+'='+str(v) for k,v in case.items()])
            elif isinstance(case, str):
                url_params = case
            else:
                self.ruce_log('[ CASE TYPE ERROR ]', level='error')
        host = self.config.env[env_name]
        if self.uri.startswith('/'):
            url = host + self.uri
        else:
            url = '%s/%s' % (host, self.uri)
        if url_params:
            url = '%s?%s' % (url, url_params)
        return url

    def assert_good_equal(self, text):
        assert len(self.result_list['good']) > 0
        for res in self.result_list['good']:
            assert res['body'] == text, 'result not equal'

    def assert_good_find(self, text):
        regex = re.compile(r'%s' % text)
        assert len(self.result_list['good']) > 0
        for res in self.result_list['good']:
            assert len(regex.findall(res['body'])) > 0, 'result not find'

    def assert_bad_equal(self, text):
        assert len(self.result_list['bad']) > 0
        for res in self.result_list['bad']:
            assert res['body'] == text, 'result not equal'

    def assert_bad_find(self, text):
        regex = re.compile(r'%s' % text)
        assert len(self.result_list['bad']) > 0
        for res in self.result_list['bad']:
            assert len(regex.findall(res['body'])) > 0, 'result not find'

if __name__=='__main__':
    pass

