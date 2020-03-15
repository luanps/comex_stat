# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import pdb

class Preproc:

    def __init__(self, data, columns_to_drop, uf_drop_list):
        self.data = data.copy()
        self.columns_to_drop = columns_to_drop
        self.uf_drop_list = uf_drop_list


    def drop_columns(self):
        self.data.drop(self.columns_to_drop,axis=1, inplace=True)


    def drop_non_uf(self):
        self.data = self.data[~self.data['SG_UF_NCM'].isin(self.uf_drop_list)]


    def drop_zero_vlfob(self):
        self.data = self.data[self.data['VL_FOB'] != 0]


    def keep_top_data_to_predict(self, grouped_uf, uf):
        data = self.data[self.data['SG_UF_NCM'] == uf]
        data = pd.merge(data, grouped_uf, how='inner', 
                          on=['CO_MES', 'CO_NCM'])
        self.data = data


    def target_log(self):
        self.data['log_vlfob'] = np.log(self.data['VL_FOB'])


    def merge_uf_data(self, uf_data):
        self.data = pd.merge(self.data, uf_data, how='left', 
                          left_on='SG_UF_NCM', right_on='SG_UF')


    def merge_ncm_data(self, ncm_data):
        self.data = pd.merge(self.data, ncm_data, how='left', on='CO_NCM')

    def merge_country_data(self, country_data):
        self.data = pd.merge(self.data, country_data, how='left', on='CO_PAIS')
    
    def cut_title(self, cut_point):
        self.data.loc[:,'NO_NCM_POR'] = self.data['NO_NCM_POR'].apply(lambda x: x[:cut_point])


    def apply_general_preproc(self, uf_data, ncm_data, country_data, cut_point):
        self.drop_non_uf()
        self.merge_uf_data(uf_data)
        self.merge_ncm_data(ncm_data)
        self.merge_country_data(country_data)
        self.cut_title(cut_point)
        self.drop_columns()


    def get_top_products_by_year(self,n):
        grouped = self.data.groupby(['CO_ANO', 'NO_UF', 'NO_NCM_POR', 'SG_UF_NCM', 'CO_NCM'])['CO_NCM']\
                      .count().reset_index(name='count')\
                      .sort_values(['CO_ANO', 'NO_UF', 'count'],ascending = False)
        top_grouped = grouped.groupby(['NO_UF', 'CO_ANO']).apply(lambda x: x.head(n))
        
        return top_grouped.reset_index(drop=True)


    def get_top_products_by_month(self, year, n):
        data = self.data[self.data['CO_ANO']==year]
        grouped = data.groupby(['CO_MES', 'NO_UF', 'CO_NCM', 'NO_NCM_POR'])['CO_NCM']\
                      .count().reset_index(name='count')\
                      .sort_values(['CO_MES', 'NO_UF', 'count'],ascending = False)
        top_grouped = grouped.groupby(['NO_UF', 'CO_MES']).apply(lambda x: x.head(n))

        return top_grouped.reset_index(drop=True)


    def get_summed_values_by_uf(self, year):
        data = self.data[self.data['CO_ANO']==year]
        grouped = data.groupby(['NO_REGIAO','NO_UF'])['VL_FOB']\
                      .count().reset_index(name='value')\
                      .sort_values(['value'],ascending = False)

        summ = grouped['value'].sum()
        grouped['proportion'] = grouped['value']/summ*100
        return grouped


    def get_top_products_by_month_one_uf(self, uf, n):
        data = self.data[self.data['SG_UF_NCM']==uf]
        grouped = data.groupby(['CO_MES', 'CO_NCM'])['VL_FOB']\
                      .count().reset_index(name='value')\
                      .sort_values(['CO_MES', 'value'],ascending = False)
        top_grouped = grouped.groupby(['CO_MES']).apply(lambda x: x.head(n))
        return top_grouped.reset_index(drop=True)
    

    @staticmethod
    def filter_values(data_list, attribute, values_list):
        filtered_values = list()
        for chunk in data_list:
            filtered_values.append(chunk[chunk[attribute].isin(values_list)])
        filtered_values = pd.concat(filtered_values)
        return filtered_values
