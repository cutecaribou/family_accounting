from custom_session import BasedSession
import json
from models import Person, PersonWithID
import PyQt6.QtWidgets as qw
import sys

class AddNewPersonWidget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QVBoxLayout()
        button = qw.QPushButton('Save person')
        button.clicked.connect(self.save_button)

        self.name = qw.QLineEdit()
        self.name.setMaxLength(10)
        self.name.setPlaceholderText("Введите имя")

        self.is_parent = qw.QCheckBox()
        self.is_parent.setText("is_parent")


        layout.addWidget(self.name)
        layout.addWidget(self.is_parent)
        layout.addWidget(button)

        self.setLayout(layout)
        # self.()

    def save_button(self):
        person = {
            'name': self.name.text(),
            'is_parent': self.is_parent.isChecked()
        }
        result = self.session.post('people/', json=person)
        print(result.text)