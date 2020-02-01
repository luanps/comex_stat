# -*- coding: utf-8 -*-
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

class Model:

    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name


    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)


    def predict(self, X_test):
        self.model.predict(X_test)

    
    def eval(self, y_test, y_predicted):
        pass


    def split_data(self, data):
        X = data.drop('Churn', axis=1)
        y = data[['Churn']]
        return train_test_split(X, y, test_size = 0.3, random_state = 42)

    
    def run_model(self, data):
        X_train, X_test, y_train, y_test = self.split_data(data)
        self.fit(X_train, y_train.values.ravel())
        y_predicted = self.predict(X_test)

        self.store_model()


    def store_model(self):
        pickle.dump(self.model, open(f'models/{self.model_name}.pkl','wb'))
