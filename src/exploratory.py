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


    @staticmethod
    def plot_correlation_matrix(data):
        plt.figure(figsize=(10, 8))
        plt.title(f"""Correlation matrix""")
        corr = data.apply(lambda x: pd.factorize(x)[0]).corr()
        axis = sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns,
                         linewidths=.2, cmap="YlGnBu")

        plt.savefig("plots/correlation_matrix.png")


    @staticmethod
    def plot_density(data):
        continuous_data = data.select_dtypes(exclude=['object'])
        for attribute, item in continuous_data.iteritems():
            len_unique_values = len(item.unique())
            if attribute == 'Churn' or len_unique_values <5:
                continue
            
            plt.figure(figsize=(6, 4))
            plt.title(f"{attribute} density plot")
            plt.xlabel(f"{attribute}")
            plt.ylabel("Density")
            axis0 = sns.kdeplot(data[data['Churn'] == 0][attribute], 
                              color= 'red', label= 'No Churn')
            axis1 = sns.kdeplot(data[data['Churn'] == 1][attribute], 
                              color= 'blue', label= 'Churn')
            plt.savefig(f"""plots/densityplot_{attribute}.png""")
            plt.close()


    @staticmethod
    def plot_bar(data):
        categorical_data = data.select_dtypes(exclude=['int64'])
        categorical_data['Churn'] = categorical_data['Churn'].replace({0: 'No Churn', 1: 'Churn'})

        for attribute, item in categorical_data.iteritems():
            len_unique_values = len(item.unique())
            if attribute == 'price':# or len_unique_values >5:
                continue

            plt.figure(figsize=(10, 8))
            plt.title(f"{attribute} plot")
            tmp_data = categorical_data.groupby(attribute)['Churn'].value_counts()/len(categorical_data)
            tmp_data = tmp_data.to_frame().rename({'Churn': 'percentage'}, axis=1).reset_index()
            ax = sns.barplot(x=attribute, y= 'percentage', hue = 'Churn', data= tmp_data)

            for p in ax.patches:
                ax.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')

            plt.savefig(f"plots/barplot_{attribute}.png")
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
    def plot_data(data):
        #ExploratoryAnalysis.plot_pie(data)
        ExploratoryAnalysis.plot_correlation_matrix(data)
        ExploratoryAnalysis.plot_density(data)
        ExploratoryAnalysis.plot_bar(data)
