import sys
import os
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox, QScrollArea
)


# Class for displaying the result in a separate window
class ResultWindow(QWidget):
    def __init__(self, result_text, parent=None):
        super(ResultWindow, self).__init__(parent, flags=QtCore.Qt.WindowType.Window)
        self.setWindowTitle("Result")
        self.setFixedSize(500, 400)

        image_path2 = os.path.join("C:\\Users\\onoro\\PycharmProjects\\pythonProject\\interface pictures", "result window.jpg")
        self.label_picture2 = QLabel(self)
        self.label_picture2.setGeometry(QRect(0, 0, 500, 400))
        self.label_picture2.setPixmap(QPixmap(image_path2))
        self.label_picture2.setScaledContents(True)
        self.label_picture2.setObjectName("label_picture2")

        # Create the scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setGeometry(QRect(0, 0, 500, 350))
        self.scrollArea.setStyleSheet("color: rgb(0, 0, 0);background-color: rgba(255, 255, 255, 0);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # Create the widget that will be placed inside the scroll area
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 500, 350))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Create the label to display the result text
        self.resultLabel = QLabel(result_text)
        self.resultLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        self.scrollArea.setWidget(self.resultLabel)

        # Create the layout for the scroll area contents
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.scrollArea)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.adjustSize()


# Main UI class
class Ui_MainWindow(object):

    options = {
        "cheap": {
            "floor": ['1', '2', 'All'],
            "electric_oven": ["No"],
            "furniture_pack": ["No"],
            "parking_space": ["No"],
            "balcony": ["No"]
        },
        "average": {
            "floor": ['1', '2', '3', '4', '5', 'All'],
            "electric_oven": ["No", "Yes"],
            "furniture_pack": ["No", "Yes"],
            "parking_space": ["No"]
        },
        "expensive": {
            "floor": ['1', '2', '3', '4', '5', '6', '7', 'All'],
            "electric_oven": ["Yes"],
            "furniture_pack": ["No", "Yes"],
            "parking_space": ["No", "Yes"]
        }
    }

    translator = {
        "Yes": "True",
        'No': 'False',
        'Any': 'None',
        'All': 'None'
    }

    # Function to evaluate the budget and determine house options
    def evaluateBudget(self):
        # Import here to avoid circular import
        from main import three_houses_district

        budget = self.lineEdit.text()
        house_type = self.comboBox.currentText()
        floor = self.comboBox_2.currentText()
        if floor == 'All':
            floor = self.translator[floor]
        electric_oven = self.translator[self.comboBox_3.currentText()]
        furniture_pack = self.translator[self.comboBox_4.currentText()]
        parking_space = self.translator[self.comboBox_5.currentText()]
        balcony = self.translator[self.comboBox_6.currentText()]

        # Validate budget input
        self.label_8.clear()
        if (len(budget) > 1 and budget[0] == '0') or len(budget) == 0 or not budget.isdigit() or int(budget) < 0:
            self.label_8.setText("Error: Budget must be a positive integer.")
            return

        # Evaluate the budget based on the selected house type
        if house_type == "cheap":
            method_call = f"three_houses_district.cheap({budget}, {floor}).cheap_house()"
        elif house_type == 'average':
            method_call = f"three_houses_district.average({budget}, {floor}, {electric_oven}, {furniture_pack}, {balcony}).average_house()"
        else:
            method_call = f"three_houses_district.expensive({budget}, {floor}, {furniture_pack}, {parking_space}, {balcony}).expensive_house()"

        result_text = eval(method_call)
        # Open a new window to display the results
        self.resultWindow = ResultWindow(result_text)
        self.resultWindow.show()

    # Function to update options based on selected house type
    def updateOptions(self):
        house_type = self.comboBox.currentText()

        # Temporarily disconnect the signal
        self.comboBox_2.currentTextChanged.disconnect(self.updateBalcony)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.options[house_type]["floor"])
        # Reconnect the signal
        self.comboBox_2.currentTextChanged.connect(self.updateBalcony)

        self.comboBox_3.clear()
        self.comboBox_3.addItems(self.options[house_type]["electric_oven"])

        self.comboBox_4.clear()
        self.comboBox_4.addItems(self.options[house_type]["furniture_pack"])

        self.comboBox_5.clear()
        self.comboBox_5.addItems(self.options[house_type]["parking_space"])

        self.comboBox_6.clear()
        self.comboBox_6.addItem('No')


    # Function to update balcony options based on the selected floor
    def updateBalcony(self):
        floor = self.comboBox_2.currentText()
        if self.comboBox.currentText() != 'cheap' and (floor == 'All' or (floor.isdigit() and int(floor) > 2)):
            self.comboBox_6.clear()
            self.comboBox_6.addItems(["No", "Yes", "Any"])
        else:
            self.comboBox_6.clear()
            self.comboBox_6.addItem("No")



    # Function to set up the UI elements
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(798, 504)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        image_path = os.path.join("C:\\Users\\onoro\\PycharmProjects\\pythonProject\\interface pictures", "scale_1200.jpg")
        self.label_picture = QLabel(parent=self.centralwidget)
        self.label_picture.setGeometry(QtCore.QRect(0, 0, 798, 504))
        self.label_picture.setPixmap(QtGui.QPixmap(image_path))
        self.label_picture.setScaledContents(True)
        self.label_picture.setObjectName("label_picture")

        self.label_heading = QLabel(parent=self.centralwidget)
        self.label_heading.setGeometry(QtCore.QRect(0, 0, 801, 19))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        self.label_heading.setFont(font)
        self.label_heading.setMouseTracking(False)
        self.label_heading.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_heading.setStyleSheet("color: rgb(170, 0, 0); background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        self.label_heading.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.Canada))
        self.label_heading.setObjectName("label_heading")

        self.lineEdit = QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 40, 751, 20))
        self.lineEdit.setObjectName("LineEdit Budget")
        self.lineEdit.setValidator(QIntValidator())

        self.label_1 = QLabel(parent=self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(30, 18, 100, 20))
        self.label_1.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_1.setObjectName("label_1 Enter your budget")

        self.label_2 = QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 78, 100, 20))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_2.setObjectName("label_2 Select house type")


        self.label_3 = QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 138, 100, 20))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_3.setObjectName("label_3 Select floor")

        self.label_4 = QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 198, 100, 20))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_4.setObjectName("label_4 Electric oven")

        self.label_5 = QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 258, 100, 20))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_5.setObjectName("label_5 Furniture pack")

        self.label_6 = QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 318, 100, 20))
        self.label_6.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_6.setObjectName("label_6 Parking space")

        self.label_7 = QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 378, 100, 20))
        self.label_7.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 0, 0, 200);")
        self.label_7.setObjectName("label_7 Balcony")

        self.label_8 = QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(290, 470, 400, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(170, 0, 0)")
        self.label_8.setObjectName("label_8 Error")

        self.comboBox = QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 100, 751, 20))
        self.comboBox.setObjectName("comboBox Select house type")
        self.comboBox.addItems(["cheap", "average", "expensive"])
        self.comboBox.currentTextChanged.connect(self.updateOptions)

        self.comboBox_2 = QComboBox(parent=self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 160, 751, 20))
        self.comboBox_2.setObjectName("comboBox_2 Select floor")
        self.comboBox_2.currentTextChanged.connect(self.updateBalcony)

        self.comboBox_3 = QComboBox(parent=self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(30, 220, 751, 20))
        self.comboBox_3.setObjectName("comboBox_3 Electric oven")

        self.comboBox_4 = QComboBox(parent=self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(30, 280, 751, 20))
        self.comboBox_4.setObjectName("comboBox_4 Furniture pack")


        self.comboBox_5 = QComboBox(parent=self.centralwidget)
        self.comboBox_5.setGeometry(QtCore.QRect(30, 340, 751, 20))
        self.comboBox_5.setObjectName("comboBox_5 Parking space")

        self.comboBox_6 = QComboBox(parent=self.centralwidget)
        self.comboBox_6.setGeometry(QtCore.QRect(30, 400, 751, 20))
        self.comboBox_6.setObjectName("comboBox_6 Balcony")

        # Adding a pushг button
        self.pushButton = QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 430, 751, 32))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.pushButton.setStyleSheet("color: rgb(255, 0, 0);")
        self.pushButton.setObjectName("pushButton Evaluate")
        self.pushButton.clicked.connect(self.evaluateBudget)


        # Adding a close button
        self.closeButton = QPushButton(parent=self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(768, 0, 30, 20))
        self.closeButton.setText("X")
        self.closeButton.setStyleSheet("background-color: red; color: white;")
        self.closeButton.clicked.connect(MainWindow.close)

        # Adding a minimize button
        self.minimizeButton = QPushButton(parent=self.centralwidget)
        self.minimizeButton.setGeometry(QtCore.QRect(728, 0, 30, 20))
        self.minimizeButton.setText("-")
        self.minimizeButton.setStyleSheet("background-color: gray; color: white;")
        self.minimizeButton.clicked.connect(MainWindow.showMinimized)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.updateOptions()

    # Function to set text for UI elements
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_picture.setText(_translate("MainWindow", ""))
        self.label_heading.setText(_translate("MainWindow", "Write your budget and choose the options you like to see suitable appartments"))
        self.label_1.setText(_translate("MainWindow", "Enter your budget:"))
        self.label_2.setText(_translate("MainWindow", "Select house type:"))
        self.label_3.setText(_translate("MainWindow", "Select floor:"))
        self.label_4.setText(_translate("MainWindow", "Electric oven:"))
        self.label_5.setText(_translate("MainWindow", "Furniture pack:"))
        self.label_6.setText(_translate("MainWindow", "Parking space:"))
        self.label_7.setText(_translate("MainWindow", "Balcony:"))
        self.pushButton.setText(_translate("MainWindow", "Evaluate"))
        self.label_8.setText(_translate("MainWindow", ""))

# Main application window
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)  # Remove window frame
        self.oldPos = None # Initialize variable for window movement

    # Event handler for mouse press
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    # Event handler for mouse release
    def mouseReleaseEvent(self, event):
        self.oldPos = None

    # Event handler for mouse move
    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec())





