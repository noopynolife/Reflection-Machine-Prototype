# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:46:08 2020

@author: noopy
"""


from PyQt5 import QtWidgets
from rm_interface import question_ui, rm_ui
import pandas as pd
import time

class Window(QtWidgets.QMainWindow):
    """
    Below code is from the official qt5 documentation:
    https://doc.qt.io/qt-5/designer-using-a-ui-file-python.html
    """
    
    case_id = 0
    choice = 0
    cases = None
    answers = None
    row = None
    time_start = None
    output_path = None
    
    def printResults(self, path):
        try:
            file = open(path,"w+")
            file.write(self.answers.to_csv(index=False))
            file.close()
        except:
            print("Something went wrong while printing results to csv file. The file might not have been created.")
    
    def retranslateQuestions(self):
        self.m_ui.label_titel.setText(self.cases.iloc[self.case_id]['titel'])
        
        self.m_ui.label_casus_1.setText(self.cases.iloc[self.case_id]['casus_1'])
        self.m_ui.label_casus_1.adjustSize()
        self.m_ui.label_casus_2.setText(self.cases.iloc[self.case_id]['casus_2'])
        self.m_ui.label_casus_2.adjustSize()
        self.m_ui.label_casus_3.setText(self.cases.iloc[self.case_id]['casus_3'])
        self.m_ui.label_casus_3.adjustSize()
        self.m_ui.label_casus_4.setText(self.cases.iloc[self.case_id]['casus_4'])
        self.m_ui.label_casus_4.adjustSize()
    
        self.m_ui.label_2.setText(self.cases.iloc[self.case_id]['vraag'])
        self.m_ui.label_2.adjustSize()
        self.m_ui.label_a.setText(self.cases.iloc[self.case_id]['a'])
        self.m_ui.label_a.adjustSize()
        self.m_ui.label_b.setText(self.cases.iloc[self.case_id]['b'])
        self.m_ui.label_b.adjustSize()
        self.m_ui.label_c.setText(self.cases.iloc[self.case_id]['c'])
        self.m_ui.label_c.adjustSize()
        self.m_ui.label_d.setText(self.cases.iloc[self.case_id]['d'])
        self.m_ui.label_d.adjustSize()
        self.m_ui.label_4.setText(self.cases.iloc[self.case_id]['support'])
        self.m_ui.label_4.adjustSize()
        
    def firstAttempt(self):
        self.choice = 0
        if (self.m_ui.radioButton_a.isChecked()):
            self.choice = 1
        if (self.m_ui.radioButton_b.isChecked()):
            self.choice = 2
        if (self.m_ui.radioButton_c.isChecked()):
            self.choice = 3
        if (self.m_ui.radioButton_d.isChecked()):
            self.choice = 4
            
        if (self.choice > 0):
            #print('Jouw keus was', self.choice)
            self.row = pd.Series(0, index=self.answers.columns)
            self.row["case_id"] = self.case_id
            self.row["preliminary answer"] = self.choice
            self.startRMWindow()
            
    def secondAttempt(self):
        time_stop = time.time()
        
        self.choice = 0
        if (self.m_ui.radioButton_a.isChecked()):
            self.choice = 1
        if (self.m_ui.radioButton_b.isChecked()):
            self.choice = 2
        if (self.m_ui.radioButton_c.isChecked()):
            self.choice = 3
        if (self.m_ui.radioButton_d.isChecked()):
            self.choice = 4
            
        self.row["final answer"] = self.choice
        self.row["total time"] = round(time_stop - self.time_start, 0)
        self.answers = self.answers.append(self.row, ignore_index=True)
               
        self.case_id += 1
        if (self.case_id < len(self.cases)):
            self.startQuestionWindow()
            #self.startEvaluationWindow()
            
        else:
            self.printResults(self.output_path)
            self.close()
            
    def startQuestionWindow(self):
        self.m_ui = question_ui.Ui_MainWindow()
        self.m_ui.setupUi(self)
        self.m_ui.pushButton.clicked.connect(self.firstAttempt)
        
        # Set the onscreen text
        self.retranslateQuestions()

        self.show()
        self.time_start = time.time()
        
    def startRMWindow(self):
        self.m_ui = rm_ui.Ui_MainWindow()
        self.m_ui.setupUi(self)
        self.m_ui.pushButton.clicked.connect(self.startConfirmWindow)
        
        # Set RM text
        self.m_ui.label_2.setText(self.cases.iloc[self.case_id]['rm'])
        self.m_ui.label_2.adjustSize()
        
        self.show()
        
    def startConfirmWindow(self):
        self.m_ui = question_ui.Ui_MainWindow()
        self.m_ui.setupUi(self)
        self.m_ui.pushButton.clicked.connect(self.secondAttempt)
        
        # Set previous choice
        if (self.choice == 1):
            self.m_ui.radioButton_a.setChecked(True)
        if (self.choice == 2):
            self.m_ui.radioButton_b.setChecked(True)
        if (self.choice == 3):
            self.m_ui.radioButton_c.setChecked(True)
        if (self.choice == 4):
            self.m_ui.radioButton_d.setChecked(True)

        # Set the onscreen text
        self.retranslateQuestions()
    
        self.show()

    def readCases(self, path):
        df = pd.read_csv(path, sep=";", dtype=str).fillna("")
        #df.info()
        return df
    
    def start(self, input_path, output_path):
        #try:
        self.output_path = output_path
        self.cases = self.readCases(input_path) 
        self.answers = pd.DataFrame(columns = ["case_id", "preliminary answer", "final answer","total time"], dtype=int)
        self.startQuestionWindow()
        #except:
            #print("Something went wrong while loading the supplied csv file! Cannot proceed.")

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)