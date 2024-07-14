from PyQt5 import
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget)
from PyQt5.QtCore import (
    pyqtSlot
)


Form, Window = uic.loadUiType("dialog.ui")
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Check Email Spam or Ham")
        self.resize(500, 500)

        # Create a QFormLayout instance
        layout = QFormLayout()
        layout.layout()
        # Add title to the layout
        layout.addRow("Email Spam Detection Using Python & Machine Learning", QLabel())
        # Add widgets to the layout
        btOK = QPushButton("START PROGRAM")

        btOK.clicked.connect(self.on_click)
        layout.addWidget(btOK)

        layout.addRow("Name:", QLineEdit())
        layout.addRow("Job:", QLineEdit())
        emailLabel = QLabel("Email:")
        layout.addRow(emailLabel, QLineEdit())



        # Set the layout on the application's window
        self.setLayout(layout)

    @pyqtSlot()
    def on_click(self):
        print("okok")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
