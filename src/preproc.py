# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class Preproc:

    def __init__(self):
        pass


    def clean_empty_data(self,data):
        data.drop(columns=['customerID'], inplace=True)
        data['TotalCharges'] = data['TotalCharges'].replace(' ',np.nan)
        data.dropna(inplace=True)
        return data


    def normalize_text(self, data_item):
        return data_item.str.lower()

    
    def map_binary_text(self, data_item):
        map_dict = {
                    'no': int(0),
                    'yes': (1),
                    '0': int(0),
                    '1': int(1)
                    }
        return  data_item.replace(map_dict)


    def map_str_to_float(self, data_attribute):
        data_attribute = data_attribute.astype(float)
        return data_attribute


    def apply_preproc(self,data):
        data = self.clean_empty_data(data)
        categorical_data = data.select_dtypes(include=['object'])

        for attribute, item in categorical_data.iteritems():
            normalized_item = self.normalize_text(item)
            data[attribute] = self.map_binary_text(normalized_item)

        data['TotalCharges'] = self.map_str_to_float(data['TotalCharges'])
        return data
