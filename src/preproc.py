# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class Preproc:

    def __init__(self, data, columns_to_drop, empty_spaces):
        self.data = data
        self.columns_to_drop = columns_to_drop
        self.empty_spaces = empty_spaces


    def drop_columns(self):
        self.data.drop(self.columns_to_drop,axis=1, inplace=True)


    def clean_empty_spaces(self):
        for empty in self.empty_spaces.keys():
            self.data[empty] = self.data[empty].replace(' ',np.nan)
        self.data.dropna(inplace=True)


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


    def apply_preproc(self):
        self.drop_columns()
        self.clean_empty_spaces()
        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            normalized_item = self.normalize_text(item)
            self.data[attribute] = self.map_binary_text(normalized_item)

        self.data['TotalCharges'] = self.map_str_to_float(self.data['TotalCharges'])
        return self.data


    @staticmethod
    def encode_data(data):
        encoded_data = pd.get_dummies(data)
        return encoded_data


    @staticmethod
    def split_data(data):
        X = data.drop('Churn', axis=1)
        y = data[['Churn']]
        return train_test_split(X, y, test_size = 0.3, random_state = 42)
