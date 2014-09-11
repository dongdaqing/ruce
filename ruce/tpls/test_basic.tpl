#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ruce import *

class {{name}}(RuceCase):
    def setUp(self):
        self.uri = ''
        self.method = 'GET'

    def add_good_case(self):
        ret = []
        '''
        TODO:append good case to the list ret
        '''
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
        pass

    def verify_bad_case(self):
        '''
        use assert to verify case result
        '''
        assert self.bad_results != None
        pass

if __name__== '__main__':
    unittest.main(testRunner=RuceRunner())
