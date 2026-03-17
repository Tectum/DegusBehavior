# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:23:26 2026

@author: juryl
"""

import pandas as pd

def idx_ojimetro(target_string):
    # load responses visually determined
    file = r'...\data\degusTimev3.xlsx'
    
    # read all sheets from the excel
    sheets = pd.read_excel(file, sheet_name=None, dtype=str)
    
    # lookup for the specific animals IDS across all sheets
    lookup = {}
    for sheet_name, df in sheets.items():
        colA = df.iloc[:,0].astype(str).str.strip()
        colC = df.iloc[:,3].astype(str).str.strip()
        for a, c in zip(colA, colC):
            lookup[a] = c
    # print(lookup)
    # create a dictionary with the animal ID and the respective type of response 
    values = [lookup.get(k, None) for k in target_string]
    
    # create lists with indexes for either scape or non-scape responses
    targets_escape = {'e'}
    idx_scape = [i for i, v in enumerate(values) if v in targets_escape]
    # print(idx_scape)
    targets_freeze = {'f', 'o', 't'}
    idx_freeze = [i for i, v in enumerate(values) if v in targets_freeze]
    # print(idx_freeze)
    
    return idx_scape, idx_freeze
