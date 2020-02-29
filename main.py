# -*- coding: utf-8 -*-
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pdb
from src.utils import load_dataset
from src.exploratory import ExploratoryAnalysis
from src.preproc import Preproc
from src.model import Model
pd.set_option('display.max_rows', 1000)

# TODO: remove unnecessary attributes
# TODO: remove empty prices
# TODO: remove prices outliers
# TODO: encode strings

def data_exploration(data):
    exploratory = ExploratoryAnalysis(data)
    
    data_length = exploratory.data_length()
    print(f"""This dataset contains {data_length[0]}
        samples with {data_length[1]} attributes.\n""")

    attributes = exploratory.list_attributes()
    print(f"""These attributes are:\n {attributes}""")
    
    description = exploratory.data_description()
    print(f"""Per attribute description :""")
    [print(f"""{value}\n""") for key, value in description.items()]

    null_data = exploratory.check_null()
    print(f"""Attributes with null data:\n {null_data}""")

    majority_null = exploratory.majority_nulls(0.66)
    print(f"""Attributes which more than 66% of data is null""")
    [print(key, value) for key, value in majority_null.items()]

    empty_spaces = exploratory.check_empty_spaces()
    print(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}""")
    
    zeros = exploratory.check_zeros()
    print(f"""Numerical attributes with zeros:""")
    [print(key, value) for key, value in zeros.items()]

    unique_values = exploratory.check_unique_values(10)
    print(f"""Sample of each attribute:""")
    [print(key, value) for key, value in unique_values.items()]

    singlelabel = exploratory.check_singlelabel()
    print(f"""Attribute with only one label:""")
    [print(key, value) for key, value in singlelabel.items()]
   
    return majority_null, singlelabel


if __name__ == '__main__':
    print("============= Reading data from file  =============")
    filepath = 'data/listings_full.csv'
    data = load_dataset(filepath)

    unnecessary_columns = 'unnecessary_attributes.csv'
    unnecessary_columns = load_dataset(unnecessary_columns)
    unnecessary_columns = unnecessary_columns['attributes'].values.tolist()

    print("============= Data exploration  =============")
    majority_null, singlelabel = data_exploration(data)

    print("============= Applying Preprocessing step =============")
    empty_columns = [key for key, value in {**majority_null,
                                              **singlelabel}.items()]

    columns_to_drop = unnecessary_columns + empty_columns
    print(columns_to_drop)

    '''preproc = Preproc(data, columns_to_drop)
    treated_data = preproc.apply_preproc()

    pdb.set_trace()
    print("============= Data exploration after preprocessing  =============")
    data_exploration(treated_data)'''

    '''print("============= Plotting data  =============")
    ExploratoryAnalysis.plot_data(treated_data)

    print("============= Encoding data  =============")
    encoded_data = preproc.encode_data(treated_data)

    print("=============  Running Logistic Regression  =============")
    lr_model = LogisticRegression()
    model_name = 'logistic_regression'
    model = Model(lr_model,model_name)
    model.run_model(encoded_data)'''
