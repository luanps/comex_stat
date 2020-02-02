# -*- coding: utf-8 -*-

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

class Model:

    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name


    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)


    def predict(self, X_test):
        pred = self.model.predict(X_test)
        return pred

    
    def plot_confusion_matrix(self, conf_matrix):
        labels = ['Churn', 'Not Churn']
        plt.figure(figsize=(8,6))
        sns.heatmap(conf_matrix, annot=True, fmt='',  
                    xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted labels')
        plt.ylabel('True labels')
        plt.title(f'Confusion Matrix for {self.model_name} model')
        plt.savefig(f'plots/confusion_matrix_{self.model_name}.png')
        plt.close()

    def eval(self, y_test, y_predicted):
        class_report = classification_report(y_test, y_predicted)
        print('Classification Report')
        print(class_report)

        acc_score = accuracy_score(y_test, y_predicted)
        print(f'Accuracy Score: {acc_score}')

        conf_matrix = confusion_matrix(y_test, y_predicted)
        self.plot_confusion_matrix(conf_matrix) 


    def split_data(self, data):
        X = data.drop('Churn', axis=1)
        y = data[['Churn']]
        return train_test_split(X, y, test_size = 0.3, random_state = 42)

    
    def run_model(self, data):
        X_train, X_test, y_train, y_test = self.split_data(data)
        self.fit(X_train, y_train.values.ravel())
        y_predicted = self.predict(X_test)
        self.eval(y_test, y_predicted)
        self.store_model()


    def store_model(self):
        pickle.dump(self.model, open(f'models/{self.model_name}.pkl','wb'))
