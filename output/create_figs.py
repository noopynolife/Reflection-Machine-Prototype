# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Set fonts and styles
"""
FONT_TITLE = {'family' : 'arial',
              'weight' : 'normal',
              'size'   : 12}
FONT_AXIS = {'family' : 'arial',
             'weight' : 'normal',
             'size'   : 11}
FONT_MISC = {'family' : 'arial',
             'weight' : 'normal',
             'size'   : 10}
plt.rc('font', **FONT_MISC)

HAT = ['/', '\\', '//', '\\\\'] #also supports 'x'
LINE = ['--', ':', '-.', '--', ':', '-.']
LINE_WIDTH = 2.2

DO_DIVISION = True
DIVISION_WIDTH = 1

FILE_FORMAT = '.eps'
"""
Auxilary graph function
"""
def distribution(counts_ar):
    fig, ax = plt.subplots()
    x = np.arange(16)
    for i in range(4):
        ax.bar( x=x[i*4:(i+1)*4], height=counts_ar[i*4:(i+1)*4], label="case #"+str(i+1), hatch=HAT[i])

    x = [0,1,1.5,2,3,4,5,5.5,6,7,8,9,9.5,10,11,12,13, 13.5,14,15]
    plt.xticks(x, ['a','b',"\n 1",'c','d','a','b',"\n 2",'c','d','a','b',"\n 3",'c','d','a','b',"\n 4",'c','d'])
    plt.legend()

    plt.xlabel("Answer option and case number", font=FONT_AXIS)
    plt.ylabel("Associated features (non-zero weights)", font=FONT_AXIS)
    
    return fig
"""
Produce a bar chart to show the feature distributions
"""
counts_df = pd.read_csv("feature_counts.csv", sep=';', decimal=",", index_col=0)
counts_ar = counts_df["Number of associated Keys"].values
fig = distribution(counts_ar)
fig.savefig('figs/Fig2'+FILE_FORMAT, bbox_inches='tight')

"""
Auxilary function for the distribution of confidence scores
"""
def plot_results(results, case_nr, modules):
    results = results[results['Case'] == case_nr]
    
    COL = modules
      
    for col in "abcd":
        res = results[results['Answer Option']==col]
        labels = res['Feature'].values.tolist()
        for label in labels:
            for col2 in "abcd":
                if len(results[(results['Answer Option']==col2) & (results['Feature']==label)]) == 0:
                    new_row = pd.Series(0)
                    new_row['Answer Option'] = col2
                    new_row['Feature'] = label
                    results = results.append(new_row, ignore_index=True)
    results = results.sort_values(by=["Case", "Answer Option", "Feature"]).reset_index(drop=True)        
    
    res = results[results['Answer Option']=='a']
    size = len(res)
    labels =  res['Feature'].values.tolist()
    
    x = np.arange(size)
    width = 0.20      
    fig, ax = plt.subplots()

    col = "abcd"
    offset = [x - width*1.5, x - width*0.5, x + width*0.5, x + width*1.5]
    for i in range(4):
        res = results[results['Answer Option']==col[i]][COL].values.tolist()
        ax.bar(offset[i], res, width, label=col[i], hatch=HAT[i])

    ax.axhline(y=25, linewidth=1, color='r', linestyle='dotted', label="25%")
    plt.xticks(x, labels, rotation = 90)
    plt.xlabel('Feature considered for case', font=FONT_AXIS)
    plt.ylabel('Confidence score (%)', font=FONT_AXIS)
    plt.legend()
    plt.show()
    return fig
  
"""
Load data sheet and revert case/solution sparseness
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

fig = plot_results(sheet.copy(), 1, 'm0a, m1, m2b')
fig.savefig('figs/Fig3'+FILE_FORMAT, bbox_inches='tight')


"""
Auxilary function for analysis data
"""
def compare_modules(results, ylabel):
    fig, ax = plt.subplots()
    
    columns = results.columns.values.tolist()[3:]
    columns.remove('m0a, m1, m2b')
    columns.append('m0a, m1, m2b')

    offset = results[columns].max()[0]/100*0.5
    for i in range(len(columns)):
        col = columns[i]
        results[col] = results[col]+i*offset
        ax.plot(results[col].tolist(), LINE[i], linewidth=LINE_WIDTH, label=col)

    if DO_DIVISION:
        plt.axvline(x=3.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')
        plt.axvline(x=7.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')
        plt.axvline(x=11.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')

    x = [0,1,1.5,2,3,4,5,5.5,6,7,8,9,9.5,10,11,12,13, 13.5,14,15]
    plt.xticks(x, ['a','b',"\n 1",'c','d','a','b',"\n 2",'c','d','a','b',"\n 3",'c','d','a','b',"\n 4",'c','d'])
    plt.legend()

    plt.ylabel(ylabel, font=FONT_AXIS)
    plt.xlabel('Answer option and case number', font=FONT_AXIS)
    plt.show()
    
    return fig
"""
Load analyzed data and plot
"""
sheet = pd.read_csv("statistics_per_module.csv", sep=';', decimal=",", index_col=0)
fig = compare_modules(sheet[sheet['Analysis']=='% scores below 25'].copy(), 'Average ratio of scores below 25%')
fig.savefig('figs/Fig4'+FILE_FORMAT, bbox_inches='tight')

fig = compare_modules(sheet[sheet['Analysis']=='% scores below 50'].copy(), 'Average ratio of scores below 50%')
fig.savefig('figs/Fig5'+FILE_FORMAT, bbox_inches='tight')

fig = compare_modules(sheet[sheet['Analysis']=='total non-zero features'].copy(), 'Average number of considered features')
fig.savefig('figs/Fig6'+FILE_FORMAT, bbox_inches='tight')

fig = compare_modules(sheet[sheet['Analysis']=='standard deviation'].copy(), 'Average standard deviation across trials')
fig.savefig('figs/Fig7'+FILE_FORMAT, bbox_inches='tight')

"""
Auxilary function for analysis data of variance
"""
def compare_modules(results, ylabel):
    fig, ax = plt.subplots()
    
    columns = results.columns.values.tolist()[3:]
    columns.remove('m0a, m1, m2b')
    columns.append('m0a, m1, m2b')

    offset = 0.02
    for i in range(len(columns)):
        col = columns[i]
        results[col] = results[col]+i*offset
        ax.plot(results[col].tolist(), LINE[i], linewidth=LINE_WIDTH, label=col)

    if DO_DIVISION:
        plt.axvline(x=0.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')
        plt.axvline(x=1.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')
        plt.axvline(x=2.5, linewidth=DIVISION_WIDTH, color='r', linestyle='dotted')

    x = [0, 1, 2, 3]
    plt.xticks(x, ['1', '2', '3', '4'])
    plt.legend(loc = 'upper right')

    plt.ylabel(ylabel, font=FONT_AXIS)
    plt.xlabel('Case number', font=FONT_AXIS)
    plt.show()
    
    return fig
fig = compare_modules(sheet[sheet['Analysis']=='variance'].copy(), 'Average variance between all four answers')
fig.savefig('figs/Fig8'+FILE_FORMAT, bbox_inches='tight')