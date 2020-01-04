from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *



class menu(QWidget):

    def __init__(self, header, label_one_text, label_two_text, label_three_text, label_four_text, label_five_text):
        super().__init__()

        self.header = header
        self.label_one_text = label_one_text
        self.label_two_text = label_two_text
        self.label_three_text = label_three_text
        self.label_four_text = label_four_text
        self.label_five_text = label_five_text


        self._layout = QVBoxLayout()
        self._menu = QFrame(self)  # A menu frame

        self._label_one = QPushButton(self._menu)
        self._label_one.clicked.connect(self.labelOneFunction)
        self._label_two = QPushButton(self._menu)
        self._label_two.clicked.connect(self.labelTwoFunction)
        self._label_three = QPushButton(self._menu)
        self._label_three.clicked.connect(self.labelThreeFunction)
        self._label_four = QPushButton(self._menu)
        self._label_four.clicked.connect(self.labelFourFunction)
        self._label_five = QPushButton(self._menu)
        self._label_five.clicked.connect(self.labelFiveFunction)

        self._header_label = QLabel(self)
        self._menu_button = QPushButton("Menu", self)
        self._width = 0
        self._menu_button.clicked.connect(self.toggle_animation)
        self._menu_button.move(0, 0)

        self._toggle = QPropertyAnimation(self._menu, b"maximumWidth")

        self._layout.addWidget(self._header_label)
        self._layout.addWidget(self._menu)


        self.setLayout(self._layout)

        self.setup()

    def setup(self):
        self._menu.setFrameStyle(QFrame.WinPanel | QFrame.Raised)
        self._menu.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        i = 30;
        for key, value in {self._label_one: self.label_one_text, self._label_two: self.label_two_text,
                           self._label_three: self.label_three_text, self._label_four: self.label_four_text,
                           self._label_five:
                               self.label_five_text}.items():
            # sets the value for each label
            key.move(20, i)
            i += 30
            key.setText(value)
            key.setStyleSheet('''
            color: white;
            font-style: bold;''')

        self._header_label.setText(self.header)
        self._header_label.setFixedHeight(50)
        self._header_label.setStyleSheet('''
        color: white;
        font-style: bold''')

        self._menu.setMaximumWidth(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._header_label.resize(800, 20)
        self._header_label.setAlignment(Qt.AlignCenter)
        self._menu.setStyleSheet('''
        background-color: rgb(8, 64, 67);''')
        self._header_label.setStyleSheet('''
        background-color: orange;
        ''')


    def toggle_animation(self):

        if self._width == 0:
            self._toggle.setDuration(1000)
            self._toggle.setStartValue(0)
            self._toggle.setEndValue(200)
            self._toggle.start()
            self._menu.setMaximumWidth(0)
            self._width = 200


        else:
            self._toggle.setDuration(1000)
            self._toggle.setStartValue(200)
            self._toggle.setEndValue(0)
            self._toggle.start()
            self._width = 0

    def labelOneFunction(self):
        print("works")

    def labelTwoFunction(self):
        print("works")

    def labelThreeFunction(self):
        print("works")

    def labelFourFunction(self):
        print("works")

    def labelFiveFunction(self):
        print("Works")


if __name__ == "__main__":
    app = QApplication()
    menu = menu("ROV", "Home", "Services", "Blog", "Layout", "About", )
    menu.show()
    app.exec_()
