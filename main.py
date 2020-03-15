# -*- coding: utf-8 -*-

'''from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV
from sklearn.svm import SVR'''
import logging
import numpy as np
import pandas as pd
import pdb

from src.utils import load_dataset
from src.utils import load_serialized
from src.utils import save_serialized
from src.exploratory import ExploratoryAnalysis
from src.preproc import Preproc
from src.model import Model

pd.set_option('display.max_rows', 1000)

logging.basicConfig(filename='log.txt',level=logging.INFO)
stderrLogger=logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)

def data_exploration(data):
    exploratory = ExploratoryAnalysis(data)
    draw_line = "="*79
    
    data_length = exploratory.data_length()
    logging.info(f"""This dataset contains {data_length[0]}
        samples with {data_length[1]} attributes.\n{draw_line}""")

    attributes = exploratory.list_attributes()
    logging.info(f"""These attributes are:\n {attributes}\n{draw_line}""")
    
    description = exploratory.data_description()
    logging.info(f"""Per attribute description:\n{description}\n{draw_line}""")

    null_data = exploratory.check_null()
    logging.info(f"""Attributes with null data:\n {null_data}\n{draw_line}""")

    majority_null = exploratory.majority_nulls(0.66)
    logging.info(f"""Attributes which more than 66% of data is null:\n{majority_null}\n{draw_line}""")

    empty_spaces = exploratory.check_empty_spaces()
    logging.info(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}\n{draw_line}""")
    
    zeros = exploratory.check_zeros()
    logging.info(f"""Numerical attributes with zeros:\n{zeros}\n{draw_line}""")

    unique_values = exploratory.check_unique_values(10)
    logging.info(f"""Sample of each attribute:\n{unique_values}\n{draw_line}""")

    singlelabel = exploratory.check_singlelabel()
    logging.info(f"""Attributes with only one label:\n{singlelabel}\n{draw_line}""")


def preproc_routines(p, prefix):

    draw_line = "="*79
    logging.info(f"Reading data from file\n{draw_line}")
    data = load_dataset(p['data_filepath'], chunk = True)
    uf_filepath = 'data/UF.csv'
    uf_data = load_dataset(p['uf_filepath'], chunk = False)
    ncm_filepath = 'data/NCM.csv'
    ncm_data = load_dataset(p['ncm_filepath'], chunk = False)
    country_filepath = 'data/PAIS.csv'
    country_data = load_dataset(p['country_filepath'], chunk = False)

    logging.info(f"""Filtering data to keep only 
                 {p['year_attribute']}:{p['years_to_keep']}\n{draw_line}""")
    data = Preproc.filter_values(data, p['year_attribute'], p['years_to_keep'])

    preproc = Preproc(data, p['columns_to_drop'], p['uf_drop_list'])
    preproc.apply_general_preproc(uf_data, ncm_data, country_data,
                                  p['textual_cut_point'])

    grouped_by_year = preproc.get_top_products_by_year(p['top_n'])
    logging.info(f"""Top {p['top_n']} {prefix} by UF each year
        \n{grouped_by_year.to_markdown()}\n{draw_line}""")

    grouped_by_month = preproc.get_top_products_by_month(p['year'], p['top_n'])
    logging.info(f"""Top {p['top_n']} {prefix} by UF each {p['year']}'s month
                  \n{grouped_by_month.to_markdown()}\n{draw_line}""")

    grouped_values_by_uf = preproc.get_summed_values_by_uf(p['year'])
    logging.info(f"""{prefix} values per UF in {p['year']}\n
                {grouped_values_by_uf.to_markdown()}\n{draw_line}""")

    grouped_uf = preproc.get_top_products_by_month_one_uf(p['keep_uf'], p['top_n'])
    logging.info(f"""{prefix} {p['keep_uf']} top {p['top_n']} values per month\n
                 {grouped_uf.to_markdown()}\n{draw_line}""")

    logging.info(f"Plotting data \n{draw_line}")
    ExploratoryAnalysis.plot_data(grouped_by_year, grouped_by_month,
                                  grouped_values_by_uf, p['top_n'], p['year'], prefix)


    logging.info(f"""Keep only top {p['top_n']} data per month from UF {p['keep_uf']}
                  to predict their values\n{draw_line}""")
    preproc.keep_top_data_to_predict(grouped_uf, p['keep_uf'])

    logging.info(f"Data exploration\n{draw_line}")
    data_exploration(preproc.data)


    logging.info(f"Remove empty 'VL_FOB' from data\n{draw_line}")
    preproc.drop_zero_vlfob()

    logging.info(f"Transforming target variable 'VL_FOB' into log\n{draw_line}")
    preproc.target_log()

    '''logging.info("Plotting data")
    prefix = 'after_outlier_removal'
    ExploratoryAnalysis.plot_data(preproc.data, prefix)'''

    logging.info("Data exploration after preprocessing steps\n{draw_line}")
    data_exploration(preproc.data)

    return preproc.data


def update_alphas(generic_model, model_name, model_configs, alpha, l1_ratio): 
    refined_alphas = model_configs['update_alphas'] * alpha
    refined_l1_ratios = model_configs['update_alphas'] * l1_ratio

    if model_name == 'Ridge':
        model = generic_model(alphas = refined_alphas,
                              cv = model_configs['cross_val'])

    elif model_name == 'Lasso':
        model = generic_model(alphas = refined_alphas,
                              cv = model_configs['cross_val'],
                              max_iter = model_configs['max_iter'])

    elif model_name == 'ElasticNet':

        model = generic_model(l1_ratio = refined_l1_ratios,
                              alphas = refined_alphas,
                              cv = model_configs['cross_val'],
                              max_iter = model_configs['max_iter'])

    model = Model(model, model_name, cross_val = model_configs['cross_val'])
    return model



def run_ensemble_model(generic_model, model_name,  model_configs,
                       ensemble_param_grid):

    X_train, X_test, y_train, y_test = model_configs['splitted_data']
    y_train = y_train.to_numpy().ravel()
    y_test = y_test.to_numpy().ravel()

    scorer = make_scorer(mean_squared_error, greater_is_better = False)
    model = RandomizedSearchCV(generic_model(loss='huber'),
                               ensemble_param_grid, random_state=1, n_iter=100,
                               cv=model_configs['cross_val'], verbose=0,
                               scoring = scorer)
    model = Model(model, model_name, cross_val = model_configs['cross_val'])

    model.fit(X_train, y_train)
    best_model = model.model.best_estimator_
    best_params = model.model.best_params_ 
    logging.info(f'Best {model_name} params:\n{best_params}')

    model = Model(best_model, model_name, cross_val = model_configs['cross_val'])
    rmse_train = model.fit_cross_val(X_train, y_train)
    rmse_test = model.predict_cross_val(X_test, y_test)
    logging.info(f'RMSE on training data: {rmse_train}')
    logging.info(f'RMSE on validation data: {rmse_test}')

    model.plot_feature_importances(X_test)

    filepath = f'models/{model_name}' 
    save_serialized(filepath, model)


def run_nonlinear_model(generic_model, model_name,  model_configs,
                        nonlinear_param_grid):

    X_train, X_test, y_train, y_test = model_configs['splitted_data']
    y_train = y_train.to_numpy().ravel()
    y_test = y_test.to_numpy().ravel()

    scorer = make_scorer(mean_squared_error, greater_is_better = False)
    model = RandomizedSearchCV(generic_model(),
                               nonlinear_param_grid, random_state=1, n_iter=100,
                               cv=model_configs['cross_val'], verbose=0,
                               scoring = scorer)
    model = Model(model, model_name, cross_val = model_configs['cross_val'])

    model.fit(X_train, y_train)
    best_model = model.model.best_estimator_
    best_params = model.model.best_params_ 
    logging.info(f'Best {model_name} params:\n{best_params}')

    model = Model(best_model, model_name, cross_val = model_configs['cross_val'])
    rmse_train = model.fit_cross_val(X_train, y_train)
    rmse_test = model.predict_cross_val(X_test, y_test)
    logging.info(f'RMSE on training data: {rmse_train}')
    logging.info(f'RMSE on validation data: {rmse_test}')

    filepath = f'models/{model_name}' 
    save_serialized(filepath, model)

    
def run_linear_model(generic_model, model_name,  model_configs):

    X_train, X_test, y_train, y_test = model_configs['splitted_data']
    y_train = y_train.to_numpy().ravel()
    y_test = y_test.to_numpy().ravel()

    if model_name == 'Ridge':
        model = generic_model(alphas = model_configs['initial_alphas'],
                              cv = model_configs['cross_val'])

    elif model_name == 'Lasso':
        model = generic_model(alphas = model_configs['initial_alphas'] * 0.001,
                              cv = model_configs['cross_val'],
                              max_iter = model_configs['max_iter'])

    elif model_name == 'ElasticNet':
        model = generic_model(l1_ratio = model_configs['initial_alphas'],
                              alphas = model_configs['initial_alphas'] * 0.001,
                              cv = model_configs['cross_val'],
                              max_iter = model_configs['max_iter'])

    model = Model(model, model_name, cross_val = model_configs['cross_val'])
    alpha, l1_ratio = model.fit_linear_model(X_train, y_train)
    logging.info(f'Best alpha: {alpha}')
    if model_name == 'ElasticNet':
        logging.info(f'Best l1_ratio: {l1_ratio}')


    updated_model = update_alphas(generic_model, model_name, model_configs, 
                                  alpha, l1_ratio)
    alpha, l1_ratio = updated_model.fit_linear_model(X_train, y_train)

    rmse_train = updated_model.fit_cross_val(X_train, y_train)
    rmse_test = updated_model.predict_cross_val(X_test, y_test)
    logging.info(f'RMSE on training data: {rmse_train}')
    logging.info(f'RMSE on validation data: {rmse_test}')

    keep_coefs, discarted_coefs = updated_model.plot_coefficients(X_test)
    logging.info(f"""The {model_name} model picked {keep_coefs} features
                     and eliminated {discarted_coefs} features""")

    filepath = f'models/{model_name}' 
    save_serialized(filepath, model)


if __name__ == '__main__':
    
    preproc_params = {
        'data_filepath' : 'data/EXP_COMPLETA.csv',
        'uf_filepath' : 'data/UF.csv',
        'ncm_filepath' : 'data/NCM.csv',
        'country_filepath' : 'data/PAIS.csv',

        'uf_drop_list' : ['EX', 'CB', 'MN', 'RE', 'ED', 'ND', 'ZN'],
        'years_to_keep' : [2017, 2018, 2019],
        'year_attribute' : 'CO_ANO',
        'year' : 2019,
        'textual_cut_point' : 80,

        'columns_to_drop' : ['CO_UF', 'SG_UF', 'CO_UNID_x', 'CO_VIA', 
                            'CO_UNID_y', 'CO_URF', 'QT_ESTAT', 'KG_LIQUIDO',
                            'CO_SH6', 'CO_PPE', 'CO_PPI', 'CO_FAT_AGREG',
                            'CO_CUCI_ITEM','CO_CGCE_N3', 'CO_SIIT',
                            'CO_ISIC4', 'CO_EXP_SUBSET' , 'NO_NCM_ESP',
                            'NO_NCM_ING', 'CO_PAIS', 'CO_PAIS_ISON3',
                            'CO_PAIS_ISOA3','NO_PAIS_ING','NO_PAIS_ESP'], 
        'top_n' : 3,
        'keep_uf' : 'SC'
    }

    prefix = 'exportations'
    preproc_filepath = 'data/exp_preprocessed'
    '''try:
        data = load_serialized(preproc_filepath)
        logging.info(f'Preprocessed file preproc_filepath loaded')
    except:'''
    logging.info(f'Running data preprocessment routines')

    data = preproc_routines(preproc_params, prefix)
    save_serialized(preproc_filepath, data)

    '''general_configs = {
        'splitted_data' : Model.encode_split_data(data),
        'cross_val' : 5,
        'max_iter' : 50000,
        'initial_alphas' : np.array([0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6,
                                     10, 30, 60]),
        'update_alphas' : np.array([.6, .65, .7, .75, .8, .85, .9, .95, 1.05, 
                                    1.1, 1.15, 1.25, 1.3, 1.35, 1.4])
    }

    ensemble_param_grid = {
        'n_estimators' : [100, 500, 1000],
        'learning_rate' : [0.01, 0.02, 0.05],
        'max_depth': [1, 2, 5],
        'min_samples_leaf' : [1, 5, 10],
        'min_samples_split' : [2, 5, 10]
    }

    nonlinear_param_grid = {
        'C' : [0.001, 0.01, 0.1, 1, 10],
        'gamma' : [0.001, 0.01, 0.1, 1]
    }

    ensemble_param_grid = {
        'n_estimators' : [100],
        'learning_rate' : [0.01],
        'max_depth': [1],
        'min_samples_leaf' : [1],
        'min_samples_split' : [2]
    }

    nonlinear_param_grid = {
        'C' : [1],
        'gamma' : [1]
    }

    logging.info("Running Ridge Regression")
    model = RidgeCV
    model_name = 'Ridge'
    run_linear_model(model, model_name, general_configs)
    logging.info("="*69)


    logging.info("Running Lasso Regression")
    model = LassoCV
    model_name = 'Lasso'
    run_linear_model(model, model_name, general_configs)
    logging.info("="*69)

    logging.info("Running ElasticNet Regression")
    model = ElasticNetCV
    model_name = 'ElasticNet'
    run_linear_model(model, model_name, general_configs)
    logging.info("="*69)

    logging.info("Running SVR")
    model = SVR
    model_name = 'SVR'
    run_nonlinear_model(model, model_name, general_configs,
                        nonlinear_param_grid)
    logging.info("="*69)

    logging.info("Running Gradient Boosting")
    model = GradientBoostingRegressor
    model_name = 'GradientBoosting'
    run_ensemble_model(model, model_name, general_configs, ensemble_param_grid)
    logging.info("="*69)'''
