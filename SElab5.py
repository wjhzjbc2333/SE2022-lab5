# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:57:07 2022

@author: 86182
"""

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('lab5')
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        self.text1.setFontFamily('Times New Roman')
        self.text2.setFontFamily('Times New Roman')
        self.text1.setFontPointSize(12.0)
        self.text2.setFontPointSize(12.0)
        layout = QHBoxLayout()
        layout.addWidget(self.text1)
        
        self.button1 = QPushButton('加载csv文件')
        self.button1.clicked.connect(self.openFileAction)
        self.button2 = QPushButton('等价')
        self.button2.clicked.connect(self.equalAction)
        self.button3 = QPushButton('不等价')
        self.button3.clicked.connect(self.inequalAction)
        self.button4 = QPushButton('存疑')
        self.button4.clicked.connect(self.doubtAction)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout2.addWidget(self.button3)
        layout2.addWidget(self.button4)
        layout.addLayout(layout2)
        layout.addWidget(self.text2)
        self.setLayout(layout)
        
        self.pos = 1
        self.maxPos = 0
        
        self.equalSets = []
        self.inequalPairs = []
        self.unclearPairs = []
        
        self.tempFile1 = ''
        self.tempFile2 = ''
    
    
    def clear(self):
        self.pos = 1
        self.maxPos = 0
        self.tempFile1 = ''
        self.tempFile2 = ''
        self.equalSets.clear()
        self.inequalPairs.clear()
        self.unclearPairs.clear()
    
    def openFileAction(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '*.csv')
        with open(fileName, encoding='utf-8', mode='r') as f:
            self.lines = f.readlines()
        self.filePath = fileName[0:fileName.find('output', 0, len(fileName))]
        self.maxPos = len(self.lines)
        file1, file2 = self.getFileName()
        self.tempFile1 = file1
        self.tempFile2 = file2
        self.showCode()
        
    def getFileName(self):
        if self.pos >= self.maxPos:
            self.printResult()
        else:
            line = self.lines[self.pos]
            self.pos += 1
            file1 = line[0:line.find(',', 0, len(line))]
            file2 = line[line.find(',', 0, len(line)) + 1:len(line) - 1]
            return file1, file2
    
    def showCode(self):
        filePath1 = self.filePath + self.tempFile1
        filePath2 = self.filePath + self.tempFile2
        self.text1.setText(self.tempFile1 + '\n')
        self.text2.setText(self.tempFile2 + '\n')
        data1 = ''
        data2 = ''
        with open(filePath1, encoding='utf-8', mode='r') as f1:
            data1 = f1.read()
        with open(filePath2, encoding='utf-8', mode='r') as f2:
            data2 = f2.read()
        self.text1.append(data1)
        self.text2.append(data2)
    
    def equalAction(self):
        if self.pos >= self.maxPos:
            self.printResult()
        else:
            flag = 0
            for i in range(0, len(self.equalSets)):
                if self.tempFile1 in self.equalSets[i][0]:
                    self.equalSets[i][0].add(self.tempFile2)
                    flag = 1
                    break
                elif self.tempFile2 in self.equalSets[i][0]:
                    self.equalSets[i][0].add(self.tempFile1)
                    flag = 1
                    break
            if flag == 0:
                self.equalSets.append([{self.tempFile1, self.tempFile2}, {''}])
            i = 0
            for i in range(0, len(self.equalSets)):
                if self.tempFile1 in self.equalSets[i][0]:
                    break
            for item in self.inequalPairs:
                if self.tempFile1 in item:
                    for temp in item:
                        if temp != self.tempFile1:
                            self.equalSets[i][1].add(temp)         
                if self.tempFile2 in item:
                    for temp in item:
                        if temp != self.tempFile2:
                            self.equalSets[i][1].add(temp)
            file1, file2 = self.getFileName()
            ret = self.ifAlreadyJudged(file1, file2)
            while (ret == 0 or ret == 1) and self.pos < self.maxPos:
                file1, file2 = self.getFileName()
                ret = self.ifAlreadyJudged(file1, file2)
            self.tempFile1 = file1
            self.tempFile2 = file2
            self.showCode()
    
    def inequalAction(self):
        if self.pos >= self.maxPos:
            self.printResult()
        else:
            for i in range(0, len(self.equalSets)):
                if self.tempFile1 in self.equalSets[i][0]:
                    self.equalSets[i][1].add(self.tempFile2)
                elif self.tempFile2 in self.equalSets[i][0]:
                    self.equalSets[i][1].add(self.tempFile1)   
            self.inequalPairs.append({self.tempFile1, self.tempFile2})
            file1, file2 = self.getFileName()
            ret = self.ifAlreadyJudged(file1, file2)
            while (ret == 0 or ret == 1) and self.pos < self.maxPos:
                file1, file2 = self.getFileName()
                ret = self.ifAlreadyJudged(file1, file2)
            self.tempFile1 = file1
            self.tempFile2 = file2
            self.showCode()
   
    def doubtAction(self):
        if self.pos >= self.maxPos:
            self.printResult()
        else:
            self.unclearPairs.append({self.tempFile1, self.tempFile2})
            file1, file2 = self.getFileName()
            ret = self.ifAlreadyJudged(file1, file2)
            while (ret == 0 or ret == 1) and self.pos < self.maxPos:
                file1, file2 = self.getFileName()
                ret = self.ifAlreadyJudged(file1, file2)
            self.tempFile1 = file1
            self.tempFile2 = file2
            self.showCode()
    
    def printResult(self):
        self.text1.setText('已确认完毕！')
        self.text2.setText('已确认完毕！')
        self.text1.append('等价程序对集合如下：')
        for i in range(0, len(self.equalSets)): 
            self.text1.append(str(i + 1) + '.')
            self.text1.append(str(self.equalSets[i][0]))
        self.text2.append('存疑程序对如下：')
        for i in range(0, len(self.unclearPairs)):
            self.text2.append(str(self.unclearPairs[i]))
        self.clear()
            
    def ifAlreadyJudged(self, file1, file2): 
        file1Exist = 0
        file2Exist = 0
        for i in range(0, len(self.equalSets)):
            if file1 in self.equalSets[i][0]:
                file1Exist = 1
                if file2 in self.equalSets[i][0]:
                    return 1   #equal
                elif file2 in self.equalSets[i][1]:
                    return 0
                else:
                    flag = 0
                    for j in range(0, len(self.equalSets)):
                        if file2 in self.equalSets[j][0]:
                            flag = 1
                    if flag == 1:
                        return 0  #inequal
            elif file2 in self.equalSets[i][0]:
                file2Exist = 1
                if file1 in self.equalSets[i][0]:
                    return 1
                elif file1 in self.equalSets[i][1]:
                    return 0
                else:
                    flag = 0
                    for j in range(0, len(self.equalSets)):
                        if file1 in self.equalSets[j][0]:
                            flag = 1
                    if flag == 1:
                        return 0
        
        if file1Exist == 1 and file2Exist == 0:
            return 2
        elif file1Exist == 0 and file2Exist == 1:
            return 3
        else:
            return 4
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())
