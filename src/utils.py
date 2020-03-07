# -*- coding: utf-8 -*-

import pandas as pd
import pickle

def load_dataset(filepath):
    try:
        data = pd.read_csv(filepath, sep = ';', chunksize=500000)
        return data
    except Exception as e:
        err_msg = f"""Something went wrong while loading {filepath}
                   {str(e)}"""
        raise Exception(err_msg)


def load_serialized(filepath):
    try:
        data = pickle.load(open(f'{filepath}.pkl','rb'))
        return data
    except Exception as e:
        err_msg = f"""Something went wrong while loading {filepath}
                   {str(e)}"""
        raise Exception(err_msg)


def save_serialized(filepath, data):
    try:
        pickle.dump(data, open(f'{filepath}.pkl','wb'))
    except Exception as e:
        err_msg = f"""Something went wrong while saving {filepath} to file
                   {str(e)}"""
        raise Exception(err_msg)
