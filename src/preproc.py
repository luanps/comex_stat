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

    #TODO cast totalcharges to float
    #TODO normalize text to lowercase
    #TODO map text to 0,1,2
