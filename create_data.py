# -*- coding: utf-8 -*-

"""
This script was used to produce the data that was analyzed
"""

import pandas as pd
import scipy.stats as stats

from reflection_machine.aggregators import v1, v2, v3, v4, v5
from reflection_machine.modules import m0a, m0b, m1, m2a, m2b, m3

INCLUDE_CONTROL = False

"""
Load case descriptions
"""
cases = pd.read_csv("input/case_descriptions.csv", sep=";", decimal=",", dtype=str).fillna("")

"""
Load lookup table
"""
features = pd.read_csv("input/feature_matrix.csv", sep=';', decimal=",", index_col=0)
#data = data.append(pd.read_csv("data/data_matrix.csv", sep=',', index_col=0)).fillna(0)
features = features.loc[:, ~features.columns.str.contains('^Unnamed')]

"""
Write number of keys per case/solution to .csv
"""
sheet = pd.DataFrame(columns=["Case", "Answer Option", "Number of associated Keys"])
numdata = features.to_numpy()[:16]
cases_nr = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
answers = ['a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d']
for i in range(len(numdata)):
    new_row = pd.Series(0, index=sheet.columns)
    new_row["Case"] = cases_nr[i]
    new_row["Answer Option"] = answers[i]
    new_row["Number of associated Keys"] = sum(numdata[i, 1:] != 0)
    sheet = sheet.append(new_row, ignore_index=True)
    
file = open("output/feature_counts.csv","w+")
file.write(sheet.to_csv(sep=";", decimal=",", line_terminator='\n'))
file.close()


"""
Randomize weights to simulate real-world data
"""
def pseudorandata(data):
    numdata = data.to_numpy()[:16]
    for i in range(len(numdata)):
        nr_keys = sum(numdata[i, 1:] != 0)

        lower, upper = 0.0, 1.0
        mu, sigma = 0.5, 0.5
        norm = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        row_rand = norm.rvs(nr_keys)
        i_r = 0
        for j in range(len(numdata[i, 1:])):
            if numdata[i, j+1] != 0:
                if numdata[i, j+1] > 0:
                    numdata[i, j+1] = row_rand[i_r]
                else:
                    numdata[i, j+1] = -row_rand[i_r]
                i_r += 1
    data_pseudorand = pd.DataFrame(numdata, columns=data.columns)
    data_pseudorand['diagnose'] = data['diagnose']
    return data_pseudorand

lookup = pseudorandata(features)


"""
Auxilary function for generating all RM feedback
"""
def prep_data(i):
    # Prep data
    case = ""
    case += cases.iloc[i]['casus_1'].strip().lower()
    case += cases.iloc[i]['casus_2'].strip().lower()
    case += cases.iloc[i]['casus_3'].strip().lower()
    case += cases.iloc[i]['casus_4'].strip().lower()

    support_msg = cases.iloc[i]['support']
    support_answer = support_msg.split("antwoord ")[1][0].lower()
    support = cases.iloc[i][support_answer].strip().lower()

    return case, support

"""
Auxilary function for prepping RM
"""
def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_1 = m1()
    m_1.falsify(support, user, lookup)
    m_2 = m2b()
    m_2.falsify(case, user, lookup)
    output = v5().aggregate(m_0, m_1, m_2, debug=True)
    return output

"""
Auxilary functions for writing all the data
"""
def results_case(case_nr, modules, results, sheet): 
    labels = results.columns
    results = results.fillna(0).to_numpy()    

    str_case = case_nr + 1
    for i in [0, 1, 2, 3]:
        out = list(results[i])
        
        str_answer = answers[i]
        for feature in range( len(out) ):
            if out[feature] > 0:
                filtered = sheet.loc[(sheet["Case"]==str_case) & (sheet["Answer Option"]==str_answer) & (sheet["Feature"]==labels[feature])]
                if filtered.empty: #& (sheet["Feature"]==labels[feature])
                    new_row = pd.Series(0, index=sheet.columns)
                    new_row["Case"] = str_case
                    new_row["Answer Option"] = str_answer
                    new_row["Feature"] = labels[feature]
                    new_row[modules] = round(out[feature], 4)
                    sheet = sheet.append(new_row, ignore_index=True)
                else:
                    sheet.loc[(sheet["Case"]==str_case) & (sheet["Answer Option"]==str_answer) & (sheet["Feature"]==labels[feature]), modules] = round(out[feature], 4)
            
    return sheet

def evaluate_modules(modules, sheet, plot=False):
    sheet[modules] = 0 #create a new column for this test
    for i in range(len(cases)):
        case, support = prep_data(i)

        results = pd.DataFrame()
        for choice in "abcd":
            user = cases.iloc[i][choice].strip().lower()

            # Do RM things
            output = do_modules(case, support, user, lookup)
            new_row = pd.Series(0).drop(0)
            for o in output:
                new_row[o[1]] = o[0]
            results = results.append(new_row, ignore_index=True)
        
        sheet = results_case(i, modules, results, sheet)
    return sheet


"""
Generate results per module
"""
sheet = pd.DataFrame(columns=["Case", "Answer Option", "Feature"])

def do_modules(case, support, user, lookup):
    m_0a = m0a()
    m_0a.falsify()
    output = v5().aggregate(m_0a, debug=True)
    return output
sheet = evaluate_modules("m0a", sheet)

def do_modules(case, support, user, lookup):
    m_0a = m0a()
    m_0a.falsify()
    m_0b = m0b()
    m_0b.falsify(case, lookup)
    output = v5().aggregate(m_0a, m_0b, debug=True)
    return output
sheet = evaluate_modules("m0b", sheet)

def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_1 = m1(symmetrical=False, ab=True, ba=False)
    m_1.falsify(support, user, lookup)
    if INCLUDE_CONTROL:
        output = v5().aggregate(m_0, m_1, debug=True)
    else:
        output = v5().aggregate(m_1, debug=True)
    return output
if INCLUDE_CONTROL:
    sheet = evaluate_modules("m0a, m1", sheet)
else:
    sheet = evaluate_modules("m1", sheet)

def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_2 = m2a(symmetrical=False, ab=True, ba=False)
    m_2.falsify(case, user, lookup)
    if INCLUDE_CONTROL:
        output = v5().aggregate(m_0, m_2, debug=True)
    else:
        output = v5().aggregate(m_2, debug=True)
    return output
"""#excluded from paper
if INCLUDE_CONTROL:
    sheet = evaluate_modules("m0a, m2a", sheet)
else:
    sheet = evaluate_modules("m2a", sheet)
"""
def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_2 = m2b(symmetrical=False, ab=True, ba=False)
    m_2.falsify(case, user, lookup)
    if INCLUDE_CONTROL:
        output = v5().aggregate(m_0, m_2, debug=True)
    else:
        output = v5().aggregate(m_2, debug=True)
    return output
if INCLUDE_CONTROL:
    sheet = evaluate_modules("m0a, m2", sheet)
else:
    sheet = evaluate_modules("m2", sheet)

def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_3 = m3(symmetrical=False, ab=True, ba=False)
    m_3.falsify(support, user, lookup)
    if INCLUDE_CONTROL:
        output = v5().aggregate(m_0, m_3, debug=True)
    else:
        output = v5().aggregate(m_3, debug=True)
    return output
if INCLUDE_CONTROL:
    sheet = evaluate_modules("m0a, m3", sheet)
else:
    sheet = evaluate_modules("m3", sheet)

def do_modules(case, support, user, lookup):
    m_0 = m0a()
    m_0.falsify()
    m_1 = m1(symmetrical=False, ab=True, ba=False)
    m_1.falsify(support, user, lookup)
    m_2 = m2b(symmetrical=False, ab=True, ba=False)
    m_2.falsify(case, user, lookup)
    output = v5().aggregate(m_0, m_1, m_2, debug=True)
    return output
sheet = evaluate_modules("m0a, m1, m2b", sheet)

"""
Final manipulations of data
"""
sheet = sheet.sort_values(by=["Case", "Answer Option", "Feature"]).reset_index(drop=True)
print_sheet = sheet.copy()
case = ""
answer = ""
for i in range(len(sheet)):
    c = print_sheet.at[i, "Case"]
    if case == c:
        print_sheet.at[i, "Case"] = ""
    else:
        case = c
    
    a = print_sheet.at[i, "Answer Option"]
    if answer == a:
        print_sheet.at[i, "Answer Option"] = ""
    else:
        answer = a

"""
Write to .csv file
"""
file = open("output/feedback_per_module.csv","w+")
file.write(print_sheet.to_csv(sep=";", decimal=",", line_terminator='\n'))
file.close()