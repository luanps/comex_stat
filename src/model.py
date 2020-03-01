# -*- coding: utf-8 -*-

from src.utils import save_serialized
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
'''from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve'''
from sklearn.metrics import mean_squared_error
from sklearn.metrics import make_scorer
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

class Model:

    def __init__(self, model, model_name, cross_val):
        self.model = model
        self.model_name = model_name
        self.scorer = make_scorer(mean_squared_error, greater_is_better = False) 
        self.cross_val = cross_val


    def fit(self, X_train, y_train):
        cv_score = cross_val_score(self.model, X_train, y_train,
                                   scoring = self.scorer, cv = self.cross_val)
        rmse_train = np.sqrt(-cv_score).mean()
        return rmse_train


    def predict(self, X_test, y_test):
        cv_score = cross_val_score(self.model, X_test, y_test, 
                                   scoring = self.scorer, cv = self.cross_val)
        rmse_pred = np.sqrt(-cv_score).mean()
        return rmse_pred
   

    def plot_confusion_matrix(self, conf_matrix):
        labels = ['Churn', 'No Churn']
        plt.figure(figsize=(8,6))
        sns.heatmap(conf_matrix, annot=True, fmt='',  
                    xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted labels')
        plt.ylabel('True labels')
        plt.title(f'Confusion Matrix for {self.model_name} model')
        plt.savefig(f'plots/confusion_matrix_{self.model_name}.png')
        plt.close()

    def eval(self, y_test, y_predicted):
        '''class_report = classification_report(y_test, y_predicted)
        print('Classification Report')
        print(class_report)

        acc_score = accuracy_score(y_test, y_predicted)
        print(f'Accuracy Score: {acc_score}')

        conf_matrix = confusion_matrix(y_test, y_predicted)
        self.plot_confusion_matrix(conf_matrix)'''





    def split_data(self, data):
        X = data.drop(['logPrice', 'price'], axis=1)
        y = data[['logPrice']]
        import pdb
        pdb.set_trace()

        numerical_data = X.select_dtypes(exclude=['object'])
        standard_X = StandardScaler()
        standard_X.fit(numerical_data)
        
        categorical_data = X.select_dtypes(include=['object'])
        one_hot = OneHotEncoder()

        one_hot.fit(categorical_data)

        return train_test_split(X, y, test_size = 0.3, random_state = 42)

    
    def run_model(self, data):
        X_train, X_test, y_train, y_test = self.split_data(data)

        rmse_train = self.fit(X_train, y_train.values.ravel())
        rmse_pred = self.predict(X_test, y_test.values.ravel())
        #self.eval(y_test, y_predicted)

        filepath = f'models/{self.model_name}'
        save_serialized(filepath, self.model)
