# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 22:21:32 2021

@author: Niels Cornelissen, s1002464
"""

class v1 (object):
    
    """
    Takes any number of modules and aggregates their feedback for the user
    """
    def aggregate(self, *modules, debug=False):
        critiques = []
        
        for module in modules:
            for feedback in module.getFeedback():
                if debug:
                    critiques.append( (feedback[1] / feedback[3], feedback[2]) )
                else:
                    critiques.append( (feedback[1] / feedback[3], feedback[0]) )
        critiques.sort()
        
        if debug:
            return critiques
        return critiques[0][1]
    
class v2 (object):
    
    """
    Takes any number of modules and aggregates their feedback for the user
    """
    def aggregate(self, *modules, debug=False):
        
        critiques = []
        
        for module in modules:
            for feedback in module.getFeedback():
                critiques.append( (feedback[2], feedback[0], feedback[1], feedback[3]) )
        critiques.sort()
        
        i = 0
        n = len(critiques)
        reduced = []
        while i<n:
            x = 1
            tot = ( critiques[i][2] / critiques[i][3] )
            while i+1<n and critiques[i][0] == critiques[i+1][0]:
                tot += ( critiques[i+1][2] / critiques[i+1][3] )
                i += 1
                x += 1
            confidence = tot/x
            if confidence > 0:  
                if debug:
                    reduced.append( (confidence, critiques[i][0]) )
                else:
                    reduced.append( (confidence, critiques[i][1]) )
            i += 1
        reduced.sort()
        if debug:
            return reduced
        return reduced[0][1]
    
class v3 (object):
    
    """
    Takes any number of modules and aggregates their feedback for the user
    """
    def aggregate(self, *modules, debug=False):
        
        critiques = []
        
        for module in modules:
            for feedback in module.getFeedback():
                critiques.append( (feedback[2], feedback[0], feedback[1], feedback[3]) )
        critiques.sort()
        
        i = 0
        n = len(critiques)
        reduced = []
        while i<n:
            x = 1
            tot = ( critiques[i][2], critiques[i][3] )
            while i+1<n and critiques[i][0] == critiques[i+1][0]:
                tot += ( critiques[i+1][2], critiques[i+1][3] )
                i += 1
                x += 1
            confidence = (tot[0]) / (tot[1])
            if confidence > 0:  
                if debug:
                    reduced.append( (confidence, critiques[i][0]) )
                else:
                    reduced.append( (confidence, critiques[i][1]) )
            i += 1
        reduced.sort()
        if debug:
            return reduced
        return reduced[0][1]
    
class v4 (object):
    
    """
    Takes any number of modules and aggregates their feedback for the user
    """
    def aggregate(self, *modules, debug=False):
        
        sub_reduced = []
        for module in modules:
            critiques = []
            for feedback in module.getFeedback():
                critiques.append( (feedback[2], feedback[0], feedback[1], feedback[3]) )
            critiques.sort()
            
            i = 0
            n = len(critiques)
            while i<n:
                x = 1
                tot = ( critiques[i][2], critiques[i][3] )
                while i+1<n and critiques[i][0] == critiques[i+1][0]:
                    tot += ( critiques[i+1][2], critiques[i+1][3] )
                    i += 1
                    x += 1
                sub_reduced.append( (critiques[i][0], critiques[i][1], tot[0]/tot[1]) )
                i += 1
        sub_reduced.sort()
        #print(sub_reduced)

        reduced = []
        i = 0
        n = len(sub_reduced)
        while i<n:
            x = 1
            tot = ( sub_reduced[i][2] )
            while i+1<n and sub_reduced[i][0] == sub_reduced[i+1][0]:
                tot += ( sub_reduced[i+1][2] )
                i += 1
                x += 1
            confidence = (tot)/x
            if confidence > 0:
                if debug:
                    reduced.append( (confidence, sub_reduced[i][0]) )
                else:
                    reduced.append( (confidence, sub_reduced[i][1]) )
            i += 1
        reduced.sort()
        if debug:
            return reduced
        print(reduced)
        return reduced[0][1]
    
class v5 (object):
    
    """
    Takes any number of modules and aggregates their feedback for the user
    """
    def aggregate(self, *modules, debug=False):
        
        sub_reduced = []
        for module in modules:
            critiques = []
            for feedback in module.getFeedback():
                critiques.append( (feedback[2], feedback[0], feedback[1], feedback[3]) )
            critiques.sort()
            
            i = 0
            n = len(critiques)
            while i<n:
                x = 1
                tot = ( critiques[i][2], critiques[i][3] )
                while i+1<n and critiques[i][0] == critiques[i+1][0]:
                    tot += ( critiques[i+1][2], critiques[i+1][3] )
                    i += 1
                    x += 1
                sub_reduced.append( (critiques[i][0], critiques[i][1], tot[0]/x, tot[1]/x) )
                i += 1
        sub_reduced.sort()
        #print(sub_reduced)

        reduced = []
        i = 0
        n = len(sub_reduced)
        while i<n:
            x = 1
            tot = ( sub_reduced[i][2], sub_reduced[i][3] )
            while i+1<n and sub_reduced[i][0] == sub_reduced[i+1][0]:
                tot += ( sub_reduced[i+1][2], sub_reduced[i+1][3] )
                i += 1
                x += 1
            confidence = tot[0]/tot[1]
            if confidence > 0:
                if debug:
                    reduced.append( (confidence, sub_reduced[i][0]) )
                else:
                    reduced.append( (confidence, sub_reduced[i][1]) )
            i += 1
        reduced.sort()
        if debug:
            return reduced
        print(reduced)
        return reduced[0][1]