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
        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            empty = item.str.isspace().sum()
            if empty:
                empty_spaces.update({attribute: empty})
        return empty_spaces

    
    def check_unique_values(self,n):
        unique_values = dict()
        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            top_unique = item.unique()[:n]
            unique_values.update({attribute: top_unique})
        return unique_values
