# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pdb

class Preproc:

    def __init__(self, data, columns_to_drop, country, obj_to_float,
        num_to_categories):
        self.data = data
        self.columns_to_drop = columns_to_drop
        self.country = country
        self.obj_to_float = obj_to_float
        self.num_to_categories = num_to_categories

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


    def map_str_to_float(self, data_item):
        formatted_data = data_item.str.replace(',','')
        return formatted_data.astype(float)


    def drop_another_countries(self):
        self.data = self.data[self.data['country'] == self.country]


    def drop_zero_prices(self):
        self.data = self.data[self.data['price'] != 0]
       

    def compute_zscore(self, data_item):
        z_score = (data_item - data_item.mean())/data_item.std(ddof=0)
        return z_score


    def drop_outliers(self, outliers_to_analize, thresh):
        self.drop_zero_prices()
        data = self.data[outliers_to_analize]
        for attribute, item in data.iteritems():
            z_score = self.compute_zscore(item)
            self.data = self.data[(z_score < thresh) & (z_score > -thresh)]
        return self.data


    def map_quantile(self, data_item):
        quantile = data_item.describe()
        data_item.fillna('No data', inplace=True)

        for idx, data in data_item.iteritems():
            pdb.set_trace()
            if data <= quantile['25%']:
                data_item.loc[idx] = 'Low'

            elif data > quantile['25%'] and data <= quantile['50%']:
                data_item.loc[idx] = 'Medium'

            elif data > quantile['50%'] and data <= quantile['75%']:
                data_item.loc[idx] = 'High'

            elif data > quantile['75%']:
                data_item.loc[idx] = 'Excellent'

        return data_item


    def encode_numerical_to_categories(self):
        data = self.data[self.num_to_categories]
        for attribute, item in data.iteritems():
            mapped_categories = self.map_quantile(item)
            self.data[attribute] = mapped_categories


    def apply_preproc(self):
        self.drop_another_countries()
        self.drop_columns()

        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            normalized_item = self.normalize_text(item)
            self.data[attribute] = self.clean_signs(normalized_item)
            #self.data[attribute] = self.map_binary_text(normalized_item)

        for attribute in self.obj_to_float:
            self.data[attribute] = self.map_str_to_float(self.data[attribute])
        return self.data


    @staticmethod
    def encode_data(data):
        encoded_data = pd.get_dummies(data)
        return encoded_data
