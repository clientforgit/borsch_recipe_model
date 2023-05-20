from PyQt5 import QtWidgets
import sys

from presenter import Presenter
from view import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    presenter = Presenter(w)
    presenter.run()
    app.exec_()
