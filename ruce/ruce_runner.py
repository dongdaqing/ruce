#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2013,掌阅科技
All rights reserved.

File Name: ruce_runner.py
Author: WangLichao
Created on: 2014-03-19
'''
#sys
import sys
import time
import unittest
#self
from utils import set_color
from utils import print_error
from utils import print_warning
from utils import print_success

class ColorWritelnDecorator(object):
    """修饰基于文件类型的格式化输出，带有颜色的输出
    Attributes:
        stream：格式化输入流
    """
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, name):
        '''可以方便通过self.write访问stream类中的方法
        '''
        return getattr(self.stream, name)

    def writeln(self, msg=None):
        if msg:
            print msg
        else:
            print "\r"

    def error(self, msg):
        print_error(msg)

    def warning(self, msg):
        print_warning(msg)

    def success(self, msg):
        print_success(msg)

class RuceResult(unittest.TestResult):
    '''unittest的输出结果封装
    '''
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self,stream=sys.stderr ,descriptions=1, verbosity=1):
        unittest.TestResult.__init__(self)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        description = self.getDescription(test)
        if description.find('RuceCase') == -1:
            self.stream.success('[ Run      ] ')
            self.stream.writeln(description)
        unittest.TestResult.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            description = self.getDescription(test)
            if description.find('RuceCase') == -1:
                self.stream.success('[       OK ] ')
                self.stream.writeln(self.getDescription(test))
                self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.error('[  ERROR  ] ')
            self.stream.writeln(self.getDescription(test))
            self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.error('[  FAILED  ] ')
            self.stream.writeln(self.getDescription(test))
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.warning("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln()
            self.stream.writeln(self.separator2)
            self.stream.error("%s" % err)
            self.stream.writeln()

class RuceRunner(object):
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1):
        self.stream = ColorWritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    def run(self, test):
        result = RuceResult(self.stream, self.descriptions, self.verbosity)
        self.stream.writeln("Note: Your Unit Tests Begin")
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun - 2
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        failed, errored = map(len, (result.failures, result.errors))
        self.stream.success("[  PASSED  ] %d tests" % (run - failed - errored))
        self.stream.writeln()
        if not result.wasSuccessful():
            errorsummary = ""
            if failed:
                self.stream.error("[  FAILED  ] %d tests, listed below:" % failed)
                self.stream.writeln()
                for failedtest, failederorr in result.failures:
                    self.stream.error("[  FAILED  ] %s" % failedtest)
                    self.stream.writeln()
            if errored:
                self.stream.error("[  ERRORED ] %d tests" % errored)
                for erroredtest, erorrmsg in result.errors:
                    self.stream.error("[  ERRORED ] %s" % erroredtest)
                    self.stream.writeln()
            self.stream.writeln()
        return result


if __name__=='__main__':
    pass

