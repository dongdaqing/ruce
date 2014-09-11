#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ruce import *

class getSearch(RuceCase):
    def setUp(self):
        self.uri = '/cps/getSearch'
        self.method = 'GET'

    def add_good_case(self):
        ret = []
        '''
        TODO:append good case to the list ret
        '''
        case1 = 'fid=41&p5=19&keyWord=签到&pageSize=10&currentPage=2&seo=1&vId=5710&model=T710P&channelId=0'
        ret.append(case1)
        return ret

    def add_bad_case(self):
        ret = []
        '''
        TODO:append bad case to the list ret
        '''
        return ret

    def verify_good_case(self):
        '''
        use assert to verify case result
        '''
        assert self.good_results != None
        assert self.good_results['code'] == 200
        assert 'seo' in self.good_results['body']
        pass

    def verify_bad_case(self):
        '''
        use assert to verify case result
        '''
        assert self.bad_results != None
        pass

if __name__== '__main__':
    unittest.main(testRunner=RuceRunner())
