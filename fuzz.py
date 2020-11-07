#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:28:44 2020

@author: adam

TO: 
"""
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

path = "./gd_lyl_comp_list_v01.xlsx"


leave_names = pd.read_excel(path).astype(str)
leave_names = leave_names["list_your_leave_name"]

employernames = pd.read_excel(path, sheet_name = "gd")


def fuzz_match(employername,leave_names):
    scores = process.extractBests(employername, leave_names, scorer=fuzz.token_sort_ratio)
    print("source:",employername,"\n",'target:',scores)
    print("-"*50)
    return scores


result = []   
best_match = []  
best_match_score = [] 
for employername in employernames['employername']:
    matchs = fuzz_match(employername,leave_names)
    result.append(matchs)
    best_match.append(matchs[0][0])
    best_match_score.append(matchs[0][1])


employernames["fuzz_match_companys"] = result
employernames["best_fuzz_match_company"] = best_match
employernames["best_fuzz_match_score"] = best_match_score
employernames.to_excel("fuzz_match_results.xlsx",index=False)
