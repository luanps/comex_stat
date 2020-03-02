# -*- coding: utf-8 -*-
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pdb
from src.utils import load_dataset
from src.utils import load_serialized
from src.utils import save_serialized
from src.exploratory import ExploratoryAnalysis
from src.preproc import Preproc
from src.model import Model
pd.set_option('display.max_rows', 1000)


def data_exploration(data):
    exploratory = ExploratoryAnalysis(data)
    
    data_length = exploratory.data_length()
    print("="*79)
    print(f"""This dataset contains {data_length[0]}
        samples with {data_length[1]} attributes.\n""")
    print("="*79)

    attributes = exploratory.list_attributes()
    print(f"""These attributes are:\n {attributes}""")
    print("="*79)
    
    description = exploratory.data_description()
    print(f"""Per attribute description :""")
    [print(f"""{value}\n""") for key, value in description.items()]
    print("="*79)

    null_data = exploratory.check_null()
    print(f"""Attributes with null data:\n {null_data}""")
    print("="*79)

    majority_null = exploratory.majority_nulls(0.66)
    print(f"""Attributes which more than 66% of data is null""")
    [print(key, value) for key, value in majority_null.items()]
    print("="*79)

    empty_spaces = exploratory.check_empty_spaces()
    print(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}""")
    print("="*79)
    
    zeros = exploratory.check_zeros()
    print(f"""Numerical attributes with zeros:""")
    [print(key, value) for key, value in zeros.items()]
    print("="*79)

    unique_values = exploratory.check_unique_values(10)
    print(f"""Sample of each attribute:""")
    [print(key, value) for key, value in unique_values.items()]
    print("="*79)

    singlelabel = exploratory.check_singlelabel()
    print(f"""Attributes with only one label:""")
    [print(key, value) for key, value in singlelabel.items()]
    print("="*79)
   
    return majority_null, singlelabel


def preproc_routines():

    print("="*79)
    print("============= Reading data from file  =============")
    filepath = 'data/listings_full.csv'
    data = load_dataset(filepath)
    print("="*79)

    unnecessary_columns = 'unnecessary_attributes.csv'
    unnecessary_columns = load_dataset(unnecessary_columns)
    unnecessary_columns = unnecessary_columns['attributes'].values.tolist()

    print("============= Data exploration  =============")
    majority_null, singlelabel = data_exploration(data)
    print("="*79)

    print("============= Applying Preprocessing step =============")
    empty_columns = [key for key, value in {**majority_null,
                                              **singlelabel}.items()]
    print("="*79)

    columns_to_drop = unnecessary_columns + empty_columns

    country = 'Brazil'
    obj_to_float = ['price', 'security_deposit', 'cleaning_fee',
    'extra_people', 'host_response_rate']
    print(f"""Data that will be transformed into float:\n{obj_to_float}""")
    print("="*79)

    num_to_categories = ['host_response_rate', 'review_scores_rating', 
        'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication',
        'review_scores_location', 'review_scores_value', 'reviews_per_month']
    print(f"""Numerical data that will be transformed into categories 
        [No Data, Low, Medium, High, Excellent]
        based on their own quantiles: \n{num_to_categories}""")
    print("="*79)

    text_to_counter = ['amenities', 'name', 'summary', 'space', 'description', 'access', 
    'neighborhood_overview', 'interaction', 'house_rules']
    print(f"""Textual data that will be transformed into an integer
          by counting its words:\n{text_to_counter}""")
    print("="*79)

    preproc = Preproc(data, columns_to_drop, country , obj_to_float,
        num_to_categories, text_to_counter)
    preproc.apply_general_preproc()

    print("============= Plotting data  =============")
    prefix = 'before_outlier_removal'
    ExploratoryAnalysis.plot_data(preproc.data, prefix)
    print("="*79)

    print("============= Removing outliers  =============")
    outlier_threshold = 3
    outliers_to_analize = ['price', 'accommodates', 'bathrooms', 'bedrooms',
    'beds', 'calculated_host_listings_count', 'cleaning_fee', 'extra_people',
    'guests_included', 'minimum_nights', 'security_deposit'] 
    print(f"""Numerical data which their outliers will be removed 
        (computed by z-score): \n{outliers_to_analize}""")
    preproc.drop_outliers(outliers_to_analize, outlier_threshold)
    print("="*79)

    print("========= Transforming target variable 'price' into log ========")
    preproc.log_price()
    print("="*79)

    print("============= Plotting data  =============")
    prefix = 'after_outlier_removal'
    ExploratoryAnalysis.plot_data(preproc.data, prefix)
    print("="*79)

    print("============= Data exploration after preprocessing  =============")
    data_exploration(preproc.data)
    print("="*79)

    return preproc.data


if __name__ == '__main__':

    preproc_filepath = 'data/preprocessed_data'
    try:
        data = load_serialized(preproc_filepath)
    except:
        data = preproc_routines()
        save_serialized(preproc_filepath, data)

    '''print("============= Loading preprocessed data  =============")
    print("============= Encoding data  =============")
    encoded_data = preproc.encode_data(treated_data)'''

    print("=============  Running Logistic Regression  =============")
    cross_validation = 2
    lr_model = LogisticRegression()
    model_name = 'logistic_regression'
    model = Model(lr_model,model_name, cross_validation)
    model.run_model(data)
