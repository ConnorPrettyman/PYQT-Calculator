#!/usr/bin/env python3

# Uses Python 3 & PyQT5

import sys
from functools import partial
import math

# Import PyQT Prerequisites
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

__version__ = '1.0'
__author__ = 'Connor Prettyman'

ERROR_MESSAGE = 'ERROR'

# Create OPS Handler
def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MESSAGE
    
    return result

# Create Connection between GUI & Core
class appCtrl:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignals()
    
    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)
    
    def _buildExpression(self, sub_exp):
        if self._view.displayText() == ERROR_MESSAGE:
            self._view.clearDisplay()
        
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)
    
    def _calcFactorial(self):
        dispTxt = int(self._view.displayText())
        factorial = 1
        if dispTxt < 0:
            return ERROR_MESSAGE
        else:
            for i in range(1,(dispTxt) + 1):
                factorial = factorial*i
            self._view.setDisplayText(str(factorial))
            
    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'n!', '=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        
        self._view.buttons['n!'].clicked.connect(self._calcFactorial)
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)

# Create Subclass for GUI Config
class appGUI(QMainWindow):
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(False)
        self.generalLayout.addWidget(self.display)
        self._createStatusBar()
    
    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Hint: '**' = indices.")
        self.setStatusBar(status)
    
    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
        '7': (0,0), '8': (0,1), '9': (0,2), '/': (0,3), '*': (0,4), 'C': (0,5),
        '4': (1,0), '5': (1,1), '6': (1,2), '+': (1,3), '-': (1,4),
        '1': (2,0), '2': (2,1), '3': (2,2), '(': (2,3), ')': (2,4),
        '.': (3,0), '0': (3,1), '**': (3,2), 'n!': (3,3), '=': (3,4)}
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)  
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)
    
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()
    
    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText('')
    
    def __init__(self):
        super().__init__()  # Init GUI
        self.setWindowTitle('Calculator')
        self.setFixedSize(285, 250)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()

# Client Code
def main():
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    view = appGUI()
    view.show()
    model = evaluateExpression
    appCtrl(model=model, view=view)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
