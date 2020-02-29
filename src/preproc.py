# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pdb

class Preproc:

    def __init__(self, data, columns_to_drop, country, obj_to_str):
        self.data = data
        self.columns_to_drop = columns_to_drop
        self.country = country
        self.obj_to_str = obj_to_str


    def drop_columns(self):
        self.data.drop(self.columns_to_drop,axis=1, inplace=True)


    def clean_signs(self, data_item):
        cleaned_dolar = data_item.str.replace('$','')
        cleaned_percent = cleaned_dolar.str.replace('%','')
        return cleaned_percent


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
        formatted_data = data_attribute.str.replace(',','')
        return formatted_data.astype(float)


    def drop_another_countries(self):
        self.data = self.data[self.data['country'] == self.country]


    def apply_preproc(self):
        self.drop_another_countries()
        self.drop_columns()

        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            normalized_item = self.normalize_text(item)
            self.data[attribute] = self.clean_signs(normalized_item)
            #self.data[attribute] = self.map_binary_text(normalized_item)

        for attribute in self.obj_to_str:
            self.data[attribute] = self.map_str_to_float(self.data[attribute])
        return self.data


    @staticmethod
    def encode_data(data):
        encoded_data = pd.get_dummies(data)
        return encoded_data
