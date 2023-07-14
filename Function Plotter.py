from PySide2.QtWidgets import (QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout ,
    QMessageBox,
    QLineEdit,
    QGridLayout, 
    QGroupBox,
    QSpinBox,
    QLabel)

from PySide2.QtGui import QFont
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fg

# Window class
class Windown(QWidget):
    def __init__(self):

        super().__init__()
        # window Setup 
        self.setWindowTitle("Function Plotter")
        self.setGeometry(400, 100, 600, 600)
        self.setInterface()
        # Layout setup
        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.grpbox)
        self.fig = Figure()
        self.canvas = fg(self.fig)
        self.vBox.addWidget(self.canvas)
        self.setLayout(self.vBox)
        
    # Interface desgin
    def setInterface(self):
        grid = QGridLayout()
    
        label_style = "color: #00AA00; font: 20px;"
        text1_style = "color: black; font: 20px;"
        btn_style = "color : black; font: 20px;"

        self.grpbox = QGroupBox("Please, fill all the fields")
        self.grpbox.setFont(QFont("Sanserif",13))
        self.grpbox.setStyleSheet(text1_style)
        
        self.equationLabel = QLabel("Equation")
        self.equationLabel.setStyleSheet(label_style)
        self.equationText = QLineEdit(self)
        self.equationText.setStyleSheet(text1_style)
        self.equationText.setFixedHeight(25)
        self.equationText.setFixedWidth(200)
        grid.addWidget(self.equationLabel, 0, 0)
        grid.addWidget(self.equationText, 0, 1)
        
        self.minXLabel = QLabel("Minimum X")
        self.minXLabel.setStyleSheet(label_style)
        self.minXText = QSpinBox(self)
        self.minXText.setValue(-1)
        self.minXText.setStyleSheet(text1_style)
        self.minXText.setFixedHeight(25)
        self.minXText.setFixedWidth(200)
        grid.addWidget(self.minXLabel, 1, 0)
        grid.addWidget(self.minXText, 1, 1)
        
        self.maxXLabel = QLabel("Maximum X")
        self.maxXLabel.setStyleSheet(label_style)
        self.maxXText = QSpinBox(self)
        self.maxXText.setValue(1)
        self.maxXText.setStyleSheet(text1_style)
        self.maxXText.setFixedHeight(25)
        self.maxXText.setFixedWidth(200)
        grid.addWidget(self.maxXLabel, 1, 2)
        grid.addWidget(self.maxXText, 1, 3)

        confirmBtn = QPushButton("Plot",self)
        confirmBtn.setStyleSheet(btn_style)
        confirmBtn.clicked.connect(self.plot)
        confirmBtn.setMaximumWidth(200)
        grid.addWidget(confirmBtn, 3, 1)
        self.grpbox.setLayout(grid)
        
    
    def plot(self): #Plot button
        equation = self.getText(self.equationText.text())
        xRange = self.getX(self.minXText.value(), self.maxXText.value())
        yRange = self.getY(equation, xRange)
        if xRange is None:
            QMessageBox.information(self, "Wrong input", "Make sure Max X is larger than Min X", QMessageBox.Ok)
        elif yRange == None:
            QMessageBox.information(self, "Wrong input", "Make sure the equation is a function of X, allowed operators are +, -, *, /, ^ eg:'2*x^2+x+5' ", QMessageBox.Ok)
        else:
            self.plotFunction(xRange, yRange)

    def getText(self, equation):    # Return the written and transform it to the right equation form
        return equation.replace("^", "**")
        
    
    def getX(self, min, max):   # min and max values of X
        if min >= max:
            return None 
        
        x = np.arange(min, max+1, 1)
        return x

    def getY(self, eqaution, xRange):   #evaluate th equation for every X value in the range
        try:
            y = [eval(eqaution) for x in xRange]
            return y
        except:       
            return None
        
    def plotFunction(self, xRange, yRange): # plot the function in the figure
        self.fig.clear()
        axes = self.fig.add_subplot(111)
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_title("Function Plotter")
        axes.plot(xRange, yRange)
        self.canvas.draw()

app = QApplication(sys.argv)
windown = Windown()
windown.show()
app.exec_()