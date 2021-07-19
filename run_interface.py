# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 08:22:41 2020
"""
from PyQt5 import QtWidgets
from fm_interface.interface import Window
from falsification_machine.aggregators import v5
from falsification_machine.modules import m0a, m1, m2b

import sys
import pandas as pd

class NielsWindow(Window):
    def startFMWindow(self):
        super().startFMWindow()

        # Prepare data for FM
        try:
            case = ""
            case += self.cases.iloc[self.case_id]['casus_1'].strip().lower()
            case += self.cases.iloc[self.case_id]['casus_2'].strip().lower()
            case += self.cases.iloc[self.case_id]['casus_3'].strip().lower()
            case += self.cases.iloc[self.case_id]['casus_4'].strip().lower()
        except:
            print("FM ERROR: Case description could not be interpreted.")
            return
        try:
            support_msg = self.cases.iloc[self.case_id]['support']
            support_answer = support_msg.split("antwoord ")[1][0].lower()
            support = self.cases.iloc[self.case_id][support_answer].strip().lower()
        except:
            print("FM ERROR: Support message could not be interpreted.")
            return
        try:
            abcd = "_abcd" #1 = a, 2 = b, 3 = c, 4 = d
            user = self.cases.iloc[self.case_id][abcd[self.choice]].strip().lower()
        except:
            print("FM ERROR: User diagnosis could not be interpreted.")

        # Do FM things
        m_0a = m0a()
        m_0a.falsify()
        m_1 = m1(symmetrical=False, ab=True, ba=False)
        message = ""
        message += m_1.falsify(support, user, data, verbose=True)+"\n"
        m_2 = m2b(symmetrical=False, ab=True, ba=False)
        message += m_2.falsify(case, user, data, verbose=True)+"\n"
        #m3 = ModuleTwo()
        #message += m3.falsify(case, support, data, verbose=True)+"\n"
        message = v5().aggregate(m_0a, m_1, m_2)
        
        # Set FM text
        self.m_ui.label_2.setText(message)
        self.m_ui.label_2.adjustSize()
        
        #self.show()

data = pd.read_csv("input/feature_matrix.csv", sep=';', decimal=",", index_col=0)
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

app = QtWidgets.QApplication(sys.argv)
window = NielsWindow()
window.start("input/case_descriptions.csv", "output/participant_data.csv")
app.exec_()