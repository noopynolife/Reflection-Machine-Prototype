# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 21:30:17 2020

@author: noopy
"""
import pandas as pd

df = pd.read_csv("features.csv", sep=';')
df = df.rename(columns={"primaire symptomen (kenmerkend)": "primary", "secundaire symptomen (veel voorkomend)": "secondary", "tertiaire symptomen (zeldzaam)" : "tertiary"})
df = df.fillna("")
df.info()

def generate_symptoms(df):
    symptom_set = set()
    for index, row in df.iterrows():
       
        for symptom in row['primary'].split(";"):
            symptom_set.add(symptom.strip().lower())
            
        for symptom in row['secondary'].split(";"):
            symptom_set.add(symptom.strip().lower())
    
        for symptom in row['tertiary'].split(";"):
            symptom_set.add(symptom.strip().lower())

    symptom_list = list(symptom_set)
    symptom_list.sort()
    symptom_list.remove("")
    return symptom_list


def fill_symptoms(df, matrix):
    
    for index, row in df.iterrows():
        diagnose = row['diagnose']   
        
        if (diagnose != ""):
            new_row = pd.Series(0, index=matrix.columns)
            new_row['diagnose'] = diagnose.strip().lower()
            
            for symptom in row['primary'].split(";"):
                new_row[(symptom.strip().lower())] = 1
            
            for symptom in row['secondary'].split(";"):
                new_row[(symptom.strip().lower())] = 0.75
    
            for symptom in row['tertiary'].split(";"):
                new_row[(symptom.strip().lower())] = 0.5
            
            matrix = matrix.append(new_row, ignore_index=True)

    return matrix
     
symptoms = generate_symptoms(df);
print(symptoms)
print("\n")
symptom_matrix = pd.DataFrame(columns = ["diagnose"] + symptoms)
symptom_matrix = fill_symptoms(df, symptom_matrix)
symptom_matrix[symptoms] = symptom_matrix[symptoms].apply(pd.to_numeric)
#print(symptom_matrix)

file = open("feature_matrix.csv","w+")
file.write(symptom_matrix.to_csv(sep=";", decimal=",", line_terminator='\n'))
file.close()
