# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import pdb
import random

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

        plt.savefig(f"plots/{prefix}/correlation_matrix.png",
                    bbox_inches='tight')


    @staticmethod
    def plot_hist_boxplot(data, prefix):
        continuous_data = data.select_dtypes(exclude=['object'])
        for attribute, item in continuous_data.iteritems():
            
            fig, ax =plt.subplots(1,2, figsize=(12,4))
            sns.distplot(data[attribute], color= 'blue', ax=ax[0])
            sns.boxplot(data[attribute], color= 'blue', ax=ax[1])

            plt.savefig(f"plots/{prefix}/hist_boxplot_{attribute}.png",
                        bbox_inches='tight')
            plt.close()


    @staticmethod
    def plot_bar(data, data_type, n, prefix):
        for uf in data['NO_UF'].unique():
            tmp_data = data[data['NO_UF']==uf]
            fig, ax = plt.subplots()
            plt.title(f"{uf} - top {n} {prefix} ")
            ncm_code, ncm_index = np.unique(tmp_data["NO_NCM_POR"], return_inverse=1)

            bright_palette = sns.color_palette('bright')
            pastel_palette = sns.color_palette('pastel')
            palette = bright_palette + pastel_palette
            colors = [palette[i] for i in ncm_index]

            bar_position = list()
            legend_position = list()
            pos = -1
            for i in np.arange(0, len(tmp_data)):
                if i%n:
                    pos = pos + 0.4
                else:
                    pos = pos + 0.8
                    legend_position.append(pos)
                bar_position.append(pos)

            ax.bar(bar_position, tmp_data["count"], width=0.4, align="edge",
                   ec="k", color=colors)

            handles=[plt.Rectangle((0,0),1,1, color=palette[i], ec="k") 
                     for i in range(len(ncm_code))]

            ax.legend(handles=handles, labels=list(ncm_code), 
                      prop = {'size':10}, loc= 'center left',
                      bbox_to_anchor=(1.0, 0.5))

            ax.set_xticks(legend_position)
            ax.set_xticklabels(tmp_data[data_type].unique())
            
            plt.savefig(f"plots/{prefix}/barplot_{data_type}_{uf}.png",
                        bbox_inches='tight')
            plt.close()


    @staticmethod
    def plot_pie_per_region(data, year, prefix):
            for region in data['NO_REGIAO'].unique():
                tmp_data = data[data['NO_REGIAO']==region]
                sizes = tmp_data['value']
                summ = np.sum(sizes)
                labels = tmp_data['NO_UF']
                labels = ['%s, %1.1f %%' % (l, s) for l, s in zip(labels,
                    sizes/summ*100)] 

                plt.figure(figsize=(10, 8))
                plt.pie(sizes, labels=labels)
                plt.title(f"{prefix} values per UF from {region} in {year}")
                plt.savefig(f"plots/{prefix}/piechart_values_{region}_{year}.png",
                            bbox_inches='tight')
                plt.close()


    @staticmethod
    def plot_pie(data, year, prefix):
            tmp_data = data.groupby('NO_REGIAO').sum().reset_index()
            sizes = tmp_data['value']
            summ = np.sum(sizes)
            labels = tmp_data['NO_REGIAO']
            labels = ['%s, %1.1f %%' % (l, s) for l, s in zip(labels,
                sizes/summ*100)] 

            plt.figure(figsize=(10, 8))
            plt.pie(sizes, labels=labels)
            plt.title(f"{prefix} values per region in {year}")
            plt.savefig(f"plots/{prefix}/piechart_values_per_region_{year}.png",
                        bbox_inches='tight')
            plt.close()


    @staticmethod
    def plot_data(data_by_year, data_by_month, data_by_uf_values, n, year, prefix):
        #ExploratoryAnalysis.plot_correlation_matrix(data, prefix)
        #ExploratoryAnalysis.plot_hist_boxplot(data, prefix)
        ExploratoryAnalysis.plot_bar(data_by_year ,'CO_ANO', n, prefix)
        ExploratoryAnalysis.plot_bar(data_by_month ,'CO_MES', n, prefix)
        #ExploratoryAnalysis.plot_pie_per_region(data_by_uf_values, year, prefix)
        #ExploratoryAnalysis.plot_pie(data_by_uf_values, year, prefix)
