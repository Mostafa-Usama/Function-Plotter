import sys
import numpy as np
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QLineEdit,
    QGridLayout,
    QGroupBox,
    QSpinBox,
    QLabel,
)
from PySide2.QtGui import QFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(400, 100, 600, 600)
      
        self.setInterface()

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.grpbox)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.vBox.addWidget(self.canvas)
        self.setLayout(self.vBox)

    def setInterface(self):
        grid = QGridLayout()

        label_style = "color: #00AA00; font: 20px;"
        text1_style = "color: black; font: 20px;"
        btn_style = "color : black; font: 20px;"

        self.grpbox = QGroupBox("Please fill in all the fields")
        self.grpbox.setFont(QFont("SansSerif", 13))
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
        self.minXText.setRange(-1000,1000)
        self.minXText.setValue(-1)
        self.minXText.setStyleSheet(text1_style)
        self.minXText.setFixedHeight(25)
        self.minXText.setFixedWidth(200)
        grid.addWidget(self.minXLabel, 1, 0)
        grid.addWidget(self.minXText, 1, 1)

        self.maxXLabel = QLabel("Maximum X")
        self.maxXLabel.setStyleSheet(label_style)
        self.maxXText = QSpinBox(self)
        self.maxXText.setRange(-1000,1000)
        self.maxXText.setValue(1)
        self.maxXText.setStyleSheet(text1_style)
        self.maxXText.setFixedHeight(25)
        self.maxXText.setFixedWidth(200)
        grid.addWidget(self.maxXLabel, 1, 2)
        grid.addWidget(self.maxXText, 1, 3)

        self.confirmBtn = QPushButton("Plot", self)
        self.confirmBtn.setStyleSheet(btn_style)
        self.confirmBtn.clicked.connect(self.plot)
        self.confirmBtn.setMaximumWidth(200)
        grid.addWidget(self.confirmBtn, 3, 1)

        self.grpbox.setLayout(grid)

    def plot(self):
        equation = self.getText(self.equationText.text())
        self.xRange = self.getX(self.minXText.value(), self.maxXText.value())
        self.yRange = self.getY(equation, self.xRange)
      
        if self.xRange is None:
            QMessageBox.information(
                self,
                "Wrong input",
                "Make sure Max X is larger than Min X",
                QMessageBox.Ok,
            )
            self.error = "Make sure Max X is larger than Min X"
        
        elif self.yRange is None:
            QMessageBox.information(
                self,
                "Wrong input",
                "Make sure the equation is a function of X, allowed operators are +, -, *, /, ^ eg:'2*x^2+x+5'",
                QMessageBox.Ok,
            )
            self.error = "Make sure the equation is a function of X, allowed operators are +, -, *, /, ^ eg:'2*x^2+x+5'"
        
        else:
            self.plotFunction(self.xRange, self.yRange)

    def getText(self, equation):
        return equation.replace("^", "**")

    def getX(self, min, max):
        if min >= max:
            return None

        x = np.arange(min, max + 1, 1)
        return x

    def getY(self, equation, xRange):
        try:
            y = [eval(equation) for x in xRange]
            return y
        except:
            return None

    def plotFunction(self, xRange, yRange):
        self.fig.clear()
        axes = self.fig.add_subplot(111)
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_title("Function Plotter")
        axes.plot(xRange, yRange)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
