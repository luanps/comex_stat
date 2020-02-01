# -*- coding: utf-8 -*-
import pandas as pd
import json

from src.utils import load_dataset
from src.exploratory import ExploratoryAnalysis
from src.preproc import Preproc
if __name__ == '__main__':
    filepath = 'data/database.csv'
    data = load_dataset(filepath)

    exploratory = ExploratoryAnalysis(data)

    print(f"""The dataset {filepath} contains {exploratory.data_length()[0]}
        samples with {exploratory.data_length()[1]} attributes.\n""")
    print(f"""These attributes are:\n {exploratory.list_attributes()}""")
    print(f"""Attributes with null data:\n {exploratory.check_null()}""")

    empty_spaces = exploratory.check_empty_spaces()
    print(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}""")

    unique_values = exploratory.check_unique_values(10)
    print(f"""Sample of each attribute:""")
    [print(key, value) for key, value in unique_values.items()]

    print("============= Preprocessing =============")
    preproc = Preproc()
    data = preproc.apply_preproc(data)

    empty_spaces = exploratory.check_empty_spaces()
    print(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}""")

    unique_values = exploratory.check_unique_values(10)
    print(f"""Sample of each attribute after preprocessing step""")
    [print(key, value) for key, value in unique_values.items()]

    print(f"""Attributes after preprocessing:\n {exploratory.list_attributes()}""")

    exploratory.plot_correlation_matrix()
    exploratory.plot_density()
    exploratory.plot_bar()
