# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import pdb

class ExploratoryAnalysis:

    def __init__(self, data):
        self.data = data


    def list_attributes(self):
        return self.data.dtypes


    def data_length(self):
        return self.data.shape


    def check_null(self):
        return self.data.isnull().sum() 


    def majority_nulls(self,proportion_cutoff):
        length = self.data_length()[0]
        thresh = proportion_cutoff * length
        null = self.check_null()

        majority_nulls = dict()
        for attribute, item in null.iteritems():
            if item >= thresh:
                majority_nulls.update({attribute: item})
        return majority_nulls


    def data_description(self):
        data_description = dict()
        for attribute, item in self.data.iteritems():
            item_description = item.describe()
            data_description.update({attribute: item_description})
        return data_description


    def check_empty_spaces(self):
        empty_spaces = dict()
        categorical_data = self.data.select_dtypes(include=['object'])
        for attribute, item in categorical_data.iteritems():
            empty = item.str.isspace().sum()
            if empty:
                empty_spaces.update({attribute: empty})
        return empty_spaces


    def check_zeros(self):
        zeros = dict()
        numerical_data = self.data.select_dtypes(exclude=['object'])
        for attribute, item in numerical_data.iteritems():
            item_zero = item[item == 0].count()
            if item_zero:
                zeros.update({attribute: item_zero})
        return zeros

    
    def check_unique_values(self,n):
        unique_values = dict()
        for attribute, item in self.data.iteritems():
            top_unique = item.unique()[:n]
            unique_values.update({attribute: top_unique})
        return unique_values

    def check_singlelabel(self):
        singlelabel = dict()
        unique_values = self.check_unique_values(2)
        for key, value in unique_values.items():
            if len(value) <=1:
                singlelabel.update({key: value})
        return singlelabel


    @staticmethod
    def plot_correlation_matrix(data, prefix):
        plt.figure(figsize=(14, 14))
        plt.title(f"""Correlation matrix""")
        corr = data.apply(lambda x: pd.factorize(x)[0]).corr()
        axis = sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns,
                         linewidths=.2, cmap="YlGnBu")

        plt.savefig(f"plots/{prefix}/correlation_matrix.png")


    @staticmethod
    def plot_hist_boxplot(data, prefix):
        continuous_data = data.select_dtypes(exclude=['object'])
        for attribute, item in continuous_data.iteritems():
            
            fig, ax =plt.subplots(1,2, figsize=(12,4))
            sns.distplot(data[attribute], color= 'blue', ax=ax[0])
            sns.boxplot(data[attribute], color= 'blue', ax=ax[1])

            plt.savefig(f"plots/{prefix}/hist_boxplot_{attribute}.png")
            plt.close()



    @staticmethod
    def plot_bar(data,n, prefix):
        for state in data['SG_UF_NCM'].unique():

            plt.figure(figsize=(10, 8))
            plt.title(f"{state} - top {n} {prefix} ")
            tmp_data = data[data['SG_UF_NCM']==state].reset_index(drop=True)
            ax = sns.barplot(x='CO_ANO', y= 'count', hue = 'CO_NCM', data=tmp_data)

            for p in ax.patches:
                if not np.isnan(p.get_height()):
                    ax.annotate(int(p.get_height()),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha = 'center',
                               va = 'center',
                               xytext = (0, 5),
                               textcoords = 'offset points')

            plt.savefig(f"plots/{prefix}/barplot_{state}.png")
            plt.close()


    @staticmethod
    def plot_pie(data):
            labels = ['Churn', 'No Churn']
            sizes = data['Churn'].value_counts(sort = True)
            plt.figure(figsize=(6, 4))
            plt.title('Churn distribution')
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=270)
            plt.savefig("plots/piechart_churn.png")
            plt.close()


    @staticmethod
    def plot_data(data, n, prefix):
        #ExploratoryAnalysis.plot_pie(data)
        #ExploratoryAnalysis.plot_correlation_matrix(data, prefix)
        #ExploratoryAnalysis.plot_hist_boxplot(data, prefix)
        ExploratoryAnalysis.plot_bar(data,n, prefix)
