# -*- coding: utf-8 -*-
import pandas as pd

class ExploratoryAnalysis:

    def __init__(self, data):
        self.data = data


    def list_attributes(self):
        return self.data.keys()


    def data_length(self):
        return self.data.shape


    def check_null(self):
        return self.data.isnull().sum()


    def check_empty_spaces(self):
        empty_spaces = dict()
        for attribute, item in self.data.iteritems():
            try: 
                empty = item.str.isspace().sum()
                if empty:
                    empty_spaces.update({attribute: empty})
            except:
                #avoid non string columns
                continue
        return empty_spaces


