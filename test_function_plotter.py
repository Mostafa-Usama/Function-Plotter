import pytest
from PySide2.QtWidgets import QMessageBox
from Function_Plotter import Window
from PySide2.QtCore import Qt


@pytest.fixture
def app(qtbot):
    window = Window()
    qtbot.addWidget(window)
    return window
    

# test replacing ^ with **
def test_getText(app, qtbot):
    window = app

    qtbot.waitExposed(window)
    assert window.windowTitle() == "Function Plotter"
    assert window.getText('x^2+x^3') == 'x**2+x**3'

# test fig properties in correct input
def test_plot_function(app, qtbot):
    window = app

    window.equationText.setText("x^2 + 2*x + 1")
    window.minXText.setValue(-10)
    window.maxXText.setValue(10)

    qtbot.mouseClick(window.confirmBtn, Qt.LeftButton)

    assert window.fig.axes[0].get_title() == "Function Plotter"
    assert window.fig.axes[0].get_xlabel() == "X"
    assert window.fig.axes[0].get_ylabel() == "Y"

    
# test min x is larger that max x
def test_plot_function2(app, qtbot):
    window = app
    window.equationText.setText("x**2 + 2*x + 1")
    window.minXText.setValue(10)
    window.maxXText.setValue(0)

    qtbot.mouseClick(window.confirmBtn, Qt.LeftButton)
    
    message_box = qtbot.waitExposed(QMessageBox)
    assert window.xRange is None
    assert message_box is not None
    assert window.error == "Make sure Max X is larger than Min X"
    assert window.fig.get_axes() == []

# test equation form
def test_equation(app, qtbot):
    window = app
    window.equationText.setText("y+2")
    window.minXText.setValue(0)
    window.maxXText.setValue(10)

    qtbot.mouseClick(window.confirmBtn, Qt.LeftButton)
    assert window.yRange is None
    message_box = qtbot.waitExposed(QMessageBox)
    assert message_box is not None
    assert window.error == "Make sure the equation is a function of X, allowed operators are +, -, *, /, ^ eg:'2*x^2+x+5'"
    assert window.fig.get_axes() == []

# test that the figure has appeared
def test_plot_function3(app, qtbot):
    window = app
    window.equationText.setText("x**2 + 2*x + 1")
    window.minXText.setValue(0)
    window.maxXText.setValue(10)

    qtbot.mouseClick(window.confirmBtn, Qt.LeftButton)
    
    assert window.fig.get_axes() != []


def test_min_max(app):
    window = app
    assert window.minXLabel.text() == 'Minimum X'
    assert window.minXText.value() == -1 
    assert window.minXText.minimum() == -1000
    assert window.minXText.maximum() == 1000

    assert window.maxXLabel.text() == 'Maximum X'
    assert window.maxXText.value() == 1 
    assert window.maxXText.minimum() == -1000
    assert window.maxXText.maximum() == 1000
    