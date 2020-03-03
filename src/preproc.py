# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import pdb

class Preproc:

    def __init__(self, data, columns_to_drop, country, obj_to_float,
        num_to_categories, text_to_counter):
        self.data = data.copy()
        self.columns_to_drop = columns_to_drop
        self.country = country
        self.obj_to_float = obj_to_float
        self.num_to_categories = num_to_categories
        self.text_to_counter = text_to_counter


    def drop_columns(self):
        self.data.drop(self.columns_to_drop,axis=1, inplace=True)


    def clean_signs(self, data_item):
        lower_text = data_item.str.lower()
        cleaned_dolar = lower_text.str.replace('$','')
        cleaned_percent = cleaned_dolar.str.replace('%','')
        return cleaned_percent


    def map_str_to_float(self, data_item):
        formatted_data = data_item.str.replace(',','')
        formatted_data = formatted_data.replace('No data', np.nan)
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
        outlier_idx = list()
        for attribute, item in data.iteritems():
            z_score = self.compute_zscore(item)
            outliers =  z_score[(z_score > thresh) | (z_score < -thresh)]
            outlier_idx.append(outliers.index)
        outlier_idx = [element for sublist in outlier_idx for element in sublist] 
        outlier_idx_unique = set(outlier_idx)
        self.data = self.data.drop(outlier_idx_unique, axis=0)


    def map_numerical_to_categories(self, data_item):
        quantile = data_item.describe()
        data_item.fillna('No data', inplace=True)

        for idx, data in data_item.iteritems():
            if data == 'No data':
                continue

            elif data < quantile['25%']:
                data_item.loc[idx] = 'Low'

            elif data >= quantile['25%'] and data < quantile['50%']:
                data_item.loc[idx] = 'Medium'

            elif data >= quantile['50%'] and data < quantile['75%']:
                data_item.loc[idx] = 'High'

            elif data >= quantile['75%']:
                data_item.loc[idx] = 'Excellent'

        return data_item


    def word_count(self, data_item):
        data_item.fillna('', inplace=True)

        for idx, data in data_item.iteritems():
            filtered_data = re.sub('[^a-zA-Z\s]+', '', data)
            filtered_data = re.sub(' +', ' ',filtered_data)

            words = filtered_data.split(' ')
            data_item.loc[idx] = len(words)

        return data_item


    def word_count_amenities(self, data_item):
        data_item.fillna('', inplace=True)
        for idx, data in data_item.iteritems():
            filtered_data = re.sub('[{}"]+', '', data)

            words = filtered_data.split(',')
            data_item.loc[idx] = len(words)

        return data_item


    def log_price(self):
        self.data['logPrice'] = np.log(self.data['price'])


    def apply_general_preproc(self):
        self.drop_another_countries()
        self.drop_columns()

        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            cleaned_data = self.clean_signs(item)
            treated_data = cleaned_data.fillna('No data')
            self.data[attribute] = treated_data

        for attribute in self.obj_to_float:
            data = self.data[attribute].copy()
            self.data[attribute] = self.map_str_to_float(data)

        for attribute in self.num_to_categories:
            data = self.data[attribute].copy()
            self.data[attribute] = self.map_numerical_to_categories(data)

        for attribute in self.text_to_counter:
            data = self.data[attribute].copy()
            if attribute == 'amenities':
                self.data[attribute] = self.word_count_amenities(data)
            else:
                self.data[attribute] = self.word_count(data)

        numerical_data = self.data.select_dtypes(exclude=['object'])
        for attribute, item in numerical_data.iteritems():
            treated_data = item.fillna(0)
            self.data[attribute] = treated_data
