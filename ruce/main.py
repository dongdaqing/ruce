#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2013,掌阅科技
All rights reserved.

File Name: main.py
Author: WangLichao
Created on: 2014-03-21
'''
import os
import re
try:
    import argparse
except:
    from lib import argparse
from collections import defaultdict
import yaml
import jinja2
from jinja2 import Environment, FileSystemLoader
from pyshell import shell
from utils import print_error, print_warning, print_success, separator
__version__ = '1.1.1'

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', dest='version', help='查看版本信息',
                    action='version', version=__version__)
parser.add_argument('-e', '--env', dest='use_env',
                    help='选择执行环境', nargs='?',
                    default='')
parser.add_argument('-t', '--gen_tpl', dest='gen_tpl',
                    help='生成测试模板', nargs='?',
                    default='')
parser.add_argument('-n', '--name', dest='name',
                    help='生成测试模板', nargs='?',
                    default='all')
parser.add_argument('-c', '--gen_conf', dest='gen_conf',
                    help='生成基础测试配置文件', nargs='?',
                    default='')
options = parser.parse_args()


def parse_record(record):
    '''每个脚本执行结果汇总,并输出
    Args:
        record: 结果汇总记录
    Returns:
    Raises:
        NameError:如果参数类型不是dict会抛该异常
    '''
    passed = 0
    failed = 0
    time = 0
    for k, v in record.items():
        if v['passed']:
            passed += 1
        else:
            failed += 1
        time += v['time']
    print ('{separator}\n'
           '[ Ran {record} cases in {time} ]\n'
           '[ {passed} passed ]\n'
           '[ {failed} failed ]\n'
           '{separator}\n').format(separator=separator,
                                   record=len(record),
                                   time=time,
                                   passed=passed,
                                   failed=failed)


def parse_case(output):
    '''解析执行case输出结果
    Args:
        output: 捕获的stdout输出
    Returns:
        返回dict结构化数据
        example：
        {'passed':True,'time':0.10}
    Raises:
        IndexError: 如果split后的数据不能提取最后一项会异常
    '''
    parsed_result = {}
    parsed_result['passed'] = True
    parsed_result['time'] = 0
    err_str = ('FAIL', 'ERROR', 'Traceback', 'fail', 'error')
    for err in err_str:
        if output.find(err) > -1:
            parsed_result['passed'] = False
    regex = re.compile(r'Ran \d+ tests in \d+\.\d+s')
    time_extract = regex.search(output)
    if time_extract:
        time_used = time_extract.group().split()[-1].strip('s')
        parsed_result['time'] = float(time_used)
    return parsed_result


def run():
    '''控制脚本的执行
    Args:
    Returns:
    Raises:
        KeyError: 如果配置文件没有设置会抛异常
    '''
    use_env = options.use_env
    if use_env:
        fp = open('ruce.conf.yml.tmp', 'w')
        with open('ruce.conf.yml') as conf_file:
            config = yaml.load(conf_file)
            if use_env in config['env']:
                config['env']['use_env'] = use_env
            yaml.dump(config, stream=fp, default_flow_style=False)
            fp.close()
            ret = shell('mv ruce.conf.yml.tmp ruce.conf.yml', capture=False)
            return
    current_dir = os.path.dirname(os.path.abspath(__file__)) + '/tpls'
    j2_env = Environment(loader=FileSystemLoader(current_dir),
                         trim_blocks=True)
    case_name = options.gen_tpl
    if case_name:
        try:
            if os.path.exists('test_{}.py'.format(case_name)):
                print 'File test_{}.py has already existed'.format(case_name)
                return
            new_case = j2_env.get_template(
                'test_basic.tpl').render(name=case_name)
            create_file = open('test_{}.py'.format(case_name), 'w')
            create_file.write(new_case)
            create_file.close()
            print 'create test_{}.py ok'.format(case_name)
        except Exception as e:
            print ("gen_tpl params error\n"
                   "--gen_tpl=case_name")
        return
    if options.gen_conf:
        try:
            env_name, host_port = options.gen_conf.split('=')
            host, port = host_port.split(':')
            new_conf = j2_env.get_template('basic_conf.tpl').render(
                env_name=env_name,
                host=host,
                port=port)
            create_file = open('ruce.conf.yml', 'w')
            create_file.write(new_conf)
            create_file.close()
            print 'create ruce.conf.yml ok'
        except Exception as e:
            print ("gen_conf params error\n"
                   "--gen_conf='env_name=host:port'")
        return
    if options.name != 'all':
        name_list = options.name.split(',')
        for name in name_list:
            file_name = 'test_{}.py'.format(name.strip())
            if os.path.exists(file_name):
                ret = shell(r'python {}'.format(file_name),
                            capture=True,
                            debug=False)
                print ret.stdout
                print ret.stderr
    else:
        result_record = defaultdict(dict)
        name_list = os.listdir('.')
        print separator
        for name in name_list:
            if name.startswith('test_') and name.endswith('.py'):
                ret = shell(r'python {}'.format(name), capture=True, debug=False)
                output = ret.stdout + ret.stderr
                parsed_result = parse_case(output)
                if parsed_result['passed']:
                    print_success("{} ---- passed".format(name))
                else:
                    print_error("{} ---- failed".format(name))
                print "\r"
                result_record[name] = parsed_result
        parse_record(result_record)
    return

if __name__ == '__main__':
    run()
