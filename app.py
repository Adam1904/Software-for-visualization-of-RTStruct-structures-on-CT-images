import sys
from PyQt5 import QtWidgets

from gui import MainWindow

""" The main function """
if __name__ == "__main__":
    """
    The function that launches the application, run app by using (python app.py)
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # main window of the graphical user interface
    mainWindow.show()
    sys.exit(app.exec())
