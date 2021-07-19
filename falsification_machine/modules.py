# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 22:27:39 2021

@author: Niels Cornelissen, s1002464
"""
import pandas as pd
import re

class _module (object):    
    
    """
    A Module must support some kind falsification function that produces feedback.  
    """  
    def __init__(self):  
        self._feedback = None
    
    def falsify(self, *any_input, verbose=False):
        self._feedback = None
    
    def getFeedback(self):
        if self._feedback == None:
            raise ValueError("Falsification Machine error: getFeedback() called before falsify()")
        return self._feedback
    
class m0a (_module):
    def __init__(self):
        super().__init__()
        #self._message = "Are you sure?"
        self._message = "Weet je het zeker?"
    
    def falsify(self, *any_input, verbose=False):
        self._feedback = []
        # The most basic of feedback, with a 50% (guessing) confidence
        # tuple of (feedback, confidence, id, weight)
        self._feedback.append( (self._message, 25, self._message, 1) )
        if verbose:
            return self._message
        
class m0b (_module):
    def __init__(self):
        super().__init__()
        self._message = "Does the case mention '"
        
    def _lookup_symptoms(self, symptoms, df):
                
        symptom_list = pd.Series(0, index=df.columns)
        for i, string, in enumerate(df.columns):
            if i>0 and re.search("\W"+string+"\W",symptoms):
                symptom_list[string] = 1
 
        return symptom_list
    
    def falsify(self, case, lookup, verbose=False):
        self._feedback = []

        try:
            keywords = self._lookup_symptoms(case, lookup) #(dcs)
        except:
            return "Falsification module 0b failed to interpret given case."
        
        for i in range(len(keywords)):
            if i > 0 and keywords[i] != 0:
                key = lookup.columns[i]
                self._feedback.append( (self._message+key+"'?", 25, key, 1) )
        if verbose:
            return self._feedback[0]

class m1 (_module):
    
    def __init__(self, symmetrical=False, ab=True, ba=True):
        super().__init__()
        self._symmetrical = symmetrical
        self._ab = ab
        self._ba = ba
        self._message = "Did you consider '"
    
    def _evaluate(self, a, b, sort=False):
        tot_err, tot, inc = 0, 0, 0
        errors = [] #(error size, index)
        for i in range(1, len(a)):
            """
            For all keys in a related to keys in b
            """
            if self._symmetrical or a[i] != 0:
                """
                Add the difference in weight (according to lookup table) to error rate
                """
                err = abs(a[i] - b[i])
                if (err > 0):
                    errors.append( (1+ err/2, i) )
                    tot_err += min(err, 1)
                    #print(a[i], b[i], err, 1+abs(a[i]))
                tot += 1

        if sort:
            errors = errors.sort()
        if tot != 0:
            inc = (1 -tot_err/tot )* 100

        return inc, errors
    
    def _do_evaluate(self, a, b, df):
        analysis = ""
        
        if self._symmetrical:
            confidence, conf_errs = self._evaluate(a, b)
            for error in conf_errs:
                # tuple of (feedback, confidence, id, weight)
                key = str(df.columns[error[1]])
                self._feedback.append( (self._message+key+"'?.", confidence, key, error[0]) )
                if conf_errs:
                    analysis += "- Your solution accounts for "+str(round(confidence, 2)) +"% of key aspects I evaluated.\n"
                    conf_errs.sort()
                    analysis += "- Your solution fails to account for'"+str(df.columns[conf_errs[-1][1]])+"' (weight: "+str(conf_errs[-1][0])+").\n"
        
        if self._ab:
            accounted, acc_errs = self._evaluate(a, b)
            for error in acc_errs:
                # tuple of (feedback, confidence, id, weight)
                key = str(df.columns[error[1]])
                self._feedback.append( (self._message+key+"'?.", accounted, key, error[0]) )
                if acc_errs:
                    analysis += "- Your solution accounts for "+str(round(accounted, 2)) +"% of key aspects I evaluated.\n"
                    acc_errs.sort()
                    analysis += "- Your solution fails to account for'"+str(df.columns[acc_errs[-1][1]])+"' (weight: "+str(acc_errs[-1][0])+").\n"
        if self._ba:
            incongruent, inc_errs = self._evaluate(b, a)
            for error in inc_errs:
                # tuple of (feedback, confidence, id, weight)
                key = str(df.columns[error[1]])
                self._feedback.append( (self._message+key+"'?", incongruent, key, error[0]) )
                if inc_errs:
                    analysis += "- "+str(round(incongruent, 2)) +"% of key aspects I evaluated match with your solution.\n"
                    inc_errs.sort()
                    analysis += "- Does the case mention '"+str(df.columns[inc_errs[-1][1]])+"' (weight: "+str(inc_errs[-1][0])+")?\n"
                    
        return analysis
    
    """
    This module uses: 
        - a support solution
        - a proposed solution
        - a lookup table
    To produce a confidence level.
    """
    def falsify(self, support, user, df, verbose=False):
        self._feedback = []

        try:
            a = df.loc[df['diagnose'] == support].iloc[0]  #(dcs)
        except:
            return 'Falsification module 1 failed to interpret support solution.'

        try:
            b = df.loc[df['diagnose'] == user].iloc[0] #(e
        except:
            return 'Falsification module 1 failed to interpret user solution.'     

        analysis = "Module 1 says: Did you consider the following?\n"
        analysis += self._do_evaluate(a, b, df)
        
        if verbose:
            return analysis

class m2a (m1):
    
    def __init__(self, symmetrical=False, ab=True, ba=True):
        super().__init__(symmetrical, ab, ba)
        self._message = "Does the case mention '"
    
    def _lookup_symptoms(self, symptoms, df):
                
        symptom_list = pd.Series(0, index=df.columns)
        for i, string, in enumerate(df.columns):
            if i>0 and re.search("\W"+string+"\W",symptoms):
                symptom_list[string] = 1
 
        return symptom_list
    
    """
    This module uses: 
        - a case (problem description)
        - a proposed solution
        - a lookup table
    To produce a confidence level.
    """
    def falsify(self, symptoms, user, df, verbose=False):
        self._feedback = []

        try:
            a = self._lookup_symptoms(symptoms, df) #(dcs)
        except:
            return "Falsification module 2 failed to interpret given case."
        
        try:
            b = df.loc[df['diagnose'] == user].iloc[0]
        except:
            return 'Falsification module 2 failed to interpret given solution.'  

        analysis = "Module 2 says: Did you consider the following?\n"
        analysis += self._do_evaluate(a, b, df)
        
        if verbose:
            return analysis

class m2b (m2a):
    
    def _lookup_symptoms(self, symptoms, df):
                
        symptom_list = pd.Series(0, index=df.columns)
        for i, string, in enumerate(df.columns):
            if i>0 and re.search("\W"+string+"\W",symptoms):
                symptom_list[string] = 1
                if re.search("( niet | geen | nauwelijks | nooit | weinig ){1}[ \w]*"+string+"{1}", symptoms) or re.search(string+"{1}"+"[ \w]*( niet| geen| nauwelijks| nooit| weinig){1}", symptoms):
                    #print('- niet '+string)
                    symptom_list[string] = -symptom_list[string]

        return symptom_list
    
class m2c (m2a):
    
    def _lookup_symptoms(self, symptoms, df):
                
        symptom_list = pd.Series(0, index=df.columns, dtype=float)
        for i, string, in enumerate(df.columns):
            if i>0 and re.search("\W"+string+"\W",symptoms):
                if re.search("( erg | vaak | hevig | veel | sterk | ernstig | flink ){1}[ \w]*"+string+"{1}", symptoms) or re.search(string+"{1}"+"[ \w]*( erg| vaak| hevig| veel| sterk| ernstig| flink)", symptoms):
                    #print('- veel '+string)
                    symptom_list[string] = 1
                else:
                    #print('- '+string)
                    symptom_list[string] = 0.75
                if re.search("( niet | geen | nauwelijks | nooit | weinig ){1}[ \w]*"+string+"{1}", symptoms) or re.search(string+"{1}"+"[ \w]*( niet| geen| nauwelijks| nooit| weinig){1}", symptoms):
                    #print('- niet '+string)
                    symptom_list[string] = -symptom_list[string]

        return symptom_list
    
class m3 (m1):
    def falsify(self, generated, user, df, verbose=False):
        self._feedback = []

        try:
            a = df.loc[df['diagnose'] == generated].iloc[0]  #(dcs)
        except:
            return "Falsification module 1 failed to interpret 'generated' solution."

        try:
            b = df.loc[df['diagnose'] == user].iloc[0] #(e
        except:
            return 'Falsification module 1 failed to interpret user solution.'     

        analysis = "Module 3 says: Did you consider the following?\n"
        analysis += self._do_evaluate(a, b, df)
        
        if verbose:
            return analysis