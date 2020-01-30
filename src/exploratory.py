# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
        for attribute, item in self.data.iteritems():
            top_unique = item.unique()[:n]
            unique_values.update({attribute: top_unique})
        return unique_values


    def plot_correlation_matrix(self):
        plt.figure(figsize=(10, 8))
        plt.title(f"""Correlation matrix plot""")
        corr = self.data.apply(lambda x: pd.factorize(x)[0]).corr()
        axis = sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns,
                         linewidths=.2, cmap="YlGnBu")

        plt.savefig("data/correlation_matrix.png")


    def plot_density(self):
        continuous_data = self.data.select_dtypes(include=['float'])
        for attribute, item in continuous_data.iteritems():
            if attribute == 'Churn':
                continue
            
            plt.figure(figsize=(6, 4))
            plt.title(f"{attribute} density plot")
            plt.xlabel(f"{attribute}")
            plt.ylabel("Density")
            axis0 = sns.kdeplot(self.data[self.data['Churn'] == 0][attribute], 
                              color= 'red', label= 'No Churn')
            axis1 = sns.kdeplot(self.data[self.data['Churn'] == 1][attribute], 
                              color= 'blue', label= 'Churn')
            plt.savefig(f"""plots/{attribute}.png""")
