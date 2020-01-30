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


    def normalize_text(self, data):
        categorical_data = data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            data[attribute] = item.str.lower()
        return data

    
    def map_binary_text(self, data):
        map_dict = {'no':int(0),'yes':(1),'0':int(0),'1':int(1)}
        categorical_data = data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            data[attribute] = item.replace(map_dict)
        return data



    #TODO cast totalcharges to float
