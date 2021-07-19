# -*- coding: utf-8 -*-
import os
import pandas as pd
"""
create data n times to get more accurate data
n = the number of new datasets to generate and evaluate
"""
produce_graphs = True
runs = 50
iters = 0

path = os.getcwd()
df_concat = None
while iters < runs:
    print("Running... "+str(iters+1))
    
    """
    create a new data set
    """
    os.chdir(path) 
    exec(open("./create_data.py").read())    
    
    """
    create a new analysis
    """
    os.chdir(path+'/output/') 
    exec(open("./analyze_feedback.py").read())    
    
    """
    concatenate new analysis
    """
    df = pd.read_csv("statistics_per_module.csv", sep=';', decimal=",", index_col=0)
    if df_concat is not None:
        df_concat = pd.concat((df_concat, df))
    else:
        df_concat = df
    
    iters += 1

"""
Write average statistics to file
"""
columns = df_concat.columns.values.tolist()[3:]
by_row_index = df_concat[columns].groupby(df_concat.index)
df_means = by_row_index.mean()

sheet = pd.read_csv("statistics_per_module.csv", sep=';', decimal=",", index_col=0)
sheet[columns] = df_means[columns]
file = open("statistics_per_module.csv","w+")
file.write(sheet.to_csv(sep=";", decimal=",", line_terminator='\n'))
file.close()

"""
Produce graphs
"""
if produce_graphs:
    print("Graphing... ")
    os.chdir(path+'/output/')
    exec(open("./create_figs.py").read())