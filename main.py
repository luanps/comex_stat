# -*- coding: utf-8 -*-
import pandas as pd
import json

from src.utils import load_dataset
from src.exploratory import ExploratoryAnalysis

if __name__ == '__main__':
    filepath = 'data/database.csv'
    data = load_dataset(filepath)

    exploratory = ExploratoryAnalysis(data)
    print(f"""The dataset {filepath} contains {exploratory.data_length()[0]}
              samples with {exploratory.data_length()[1]} attributes. 
              These attributes are: {exploratory.list_attributes()}\n""")
    print(f"""Attributes with null data:\n {exploratory.check_null()}""")

    empty_spaces = exploratory.check_empty_spaces()
    print(f"""Textual attributes with empty data (value=' '):\n{empty_spaces}""")

    unique_values = exploratory.check_unique_values(10)
    print(f"""Sample of each textual attributes:""")
    [print(key, value) for key, value in unique_values.items()]
    import pdb
    pdb.set_trace()
