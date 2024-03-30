#####################        UTILITIES    ########################################



import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

import k213328


#########################     MAIN WINDOW                  ############################################################################################


class PersonalInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle('Personal Information')
        self.setGeometry(300, 300, 900, 500)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(128, 128, 128))
        palette.setColor(QPalette.Button, QColor(128, 128, 128))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        info_label = QLabel('K213328 Khuzaima Ahsan')
        info_label.setStyleSheet('color: black; font-size: 25px;')
        layout.addWidget(info_label)

        info_label = QLabel('Information Reterival')
        info_label.setStyleSheet('color: black; font-size: 25px; ')
        layout.addWidget(info_label)

        info_label = QLabel('Assignment: 01')
        info_label.setStyleSheet('color: black; font-size: 25px; ')
        layout.addWidget(info_label)

        proceed_button = QPushButton('Proceed')
        proceed_button.setStyleSheet('color: black')
        proceed_button.clicked.connect(self.openSearchWindow)
        layout.addWidget(proceed_button)

    def openSearchWindow(self):
        self.search_window = SearchWindow()
        self.search_window.show()
        self.hide()


 #######################################     QUERY WINDOW           #####################################################################



class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Information Reterival')
        self.setGeometry(300, 300, 900, 500)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(128, 128, 128))
        palette.setColor(QPalette.Button, QColor(128, 128, 128))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        query_layout = QHBoxLayout()
        layout.addLayout(query_layout)

        self.query_label = QLabel('Enter a query:')
        self.query_label.setStyleSheet('color: black')
        query_layout.addWidget(self.query_label)

        self.query_edit = QLineEdit()
        self.query_edit.setStyleSheet('background-color: white')
        query_layout.addWidget(self.query_edit)

        self.query_button = QPushButton('Process Query')
        self.query_button.setStyleSheet('color: black')
        self.query_button.clicked.connect(self.processQuery)
        layout.addWidget(self.query_button)

        self.result_label = QLabel()
        self.result_label.setStyleSheet('color: black')
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

    def processQuery(self):
        query = self.query_edit.text()
        result, time_taken = k213328.processQuery(query)
        time_taken = str(time_taken * 1000)

        if len(result) == 0:
            self.result_label.setText("Result: No results found\nTime taken: " + time_taken + " ms")
        else:
            self.result_label.setText("Result: " + str(result) + "\nTime taken: " + time_taken + " ms")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    personal_info_window = PersonalInfoWindow()
    personal_info_window.show()
    sys.exit(app.exec_())