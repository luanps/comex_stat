# -*- coding: utf-8 -*-

import pandas as pd

def load_dataset(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        err_msg = f"""Something went wrong while loading {filepath}
                   {str(e)}"""
        raise Exception(err_msg)

