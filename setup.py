#! /usr/bin/env python
#
# $Id: setup.py,v 1.0.0 2014/03/08 16:06:40 richard Exp $
import os
import sys
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
# perform the setup action

packages,data_files = [],[]

cmdclasses = {'install_data': install_data}

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def is_not_module(filename):
    return os.path.splitext(filename)[1] not in ['.py', '.pyc', '.pyo']

for ruce_dir in ['ruce','demo']:
    for dirpath, dirnames, filenames in os.walk(ruce_dir):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
            data = [f for f in filenames if is_not_module(f)]
            if data:
                data_files.append([dirpath, [os.path.join(dirpath, f) for f in data]])
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup_args = {
    'name': 'ruce',
    'version': '1.1.1',
    'description':'a http test framework',
    'long_description': open('README.txt').read(),
    'author': 'WangLichao',
    'author_email': "wanglichao@zhangyue.com",
    'packages': packages,
    'data_files': data_files,
    'include_package_data': True,
}

setup(**setup_args)
# vim: set filetype=python ts=4 sw=4 et si
