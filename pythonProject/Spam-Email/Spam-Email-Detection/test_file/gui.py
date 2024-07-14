import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from guiAI import Ui_MainWindow


def on_click():
    print("okok")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        # khai bao nut start
        self.uic.btStart.clicked.connect(on_click)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
