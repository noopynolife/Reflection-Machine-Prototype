# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

"""
Perform additional analyses on a created dataset(s)
"""
sheet = pd.read_csv("feedback_per_module.csv", sep=';', decimal=",", index_col=0)
case = ""
answer = ""
for i in range(len(sheet)):
    c = sheet.at[i, "Case"]
    if not pd.isna(c):
        case = c
    else:
        sheet.at[i, "Case"] = case
    
    a = sheet.at[i, "Answer Option"]
    if not pd.isna(a):
        answer = a
    else:
        sheet.at[i, "Answer Option"] = answer

def do_analysis(case, ans, col, sheet):
    return "foo"

def append_analysis(analysis, sheet, title):
    for case in [1 ,2, 3, 4]:
        for ans in "abcd":
            new_row = pd.Series(0, index=sheet.columns)
            new_row["Case"] = case
            new_row["Answer Option"] = ans
            new_row["Analysis"] = title
            for col in sheet.columns.values.tolist()[3:]:
                new_row[col] = do_analysis(case, ans, col, sheet)
            analysis = analysis.append(new_row, ignore_index=True)
    return analysis

analysis = pd.DataFrame(columns=["Case", "Answer Option", "Analysis"])

def do_analysis(case, ans, col, sheet):
    total = len(sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0)])
    return total
analysis = append_analysis(analysis, sheet, "total non-zero features")

def do_analysis(case, ans, col, sheet):
    total = len(sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0)])
    if total == 0:
        return 0
    b25 = len(sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0) & (sheet[col] < 25)])
    return round(b25/total * 100, 4)
analysis = append_analysis(analysis, sheet, "% scores below 25")

def do_analysis(case, ans, col, sheet):
    total = len(sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0)])
    if total == 0:
        return 0
    b50 = len(sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0) & (sheet[col] < 50)])
    return round(b50/total * 100, 4)
analysis = append_analysis(analysis, sheet, "% scores below 50")

def do_analysis(case, ans, col, sheet):
    total = sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0)]
    if len(total) <= 1:
        return 0
    return total[col].std()
analysis = append_analysis(analysis, sheet, "standard deviation")

"""
Auxilary functions for counting the variation in output
"""
def do_analysis(case, ans, col, sheet):
    total = sheet[(sheet["Case"]==case) & (sheet["Answer Option"]==ans) & (sheet[col] > 0)]
    if len(total) == 0:
        return "NONE"
    i = total[col].idxmax()
    return sheet.iloc[i]["Feature"]

def append_analysis(analysis, sheet, title):
    for case in [1 ,2, 3, 4]:
        new_row = pd.Series(0, index=sheet.columns)
        new_row["Case"] = case
        new_row["Answer Option"] = 'a, b, c, d'
        new_row["Analysis"] = title
        for col in sheet.columns.values.tolist()[3:]:
            output = []
            for ans in "abcd":
                output.append(do_analysis(case, ans, col, sheet))
            new_row[col] = len(set(output))
        analysis = analysis.append(new_row, ignore_index=True)
    return analysis


analysis = append_analysis(analysis, sheet, "variance")

analysis = analysis.drop(columns="Feature")
file = open("statistics_per_module.csv","w+")
file.write(analysis.to_csv(sep=";", decimal=",", line_terminator='\n'))
file.close()