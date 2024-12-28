from custom_session import BasedSession
import PyQt6.QtWidgets as qw
import sys

class AddNewPersonWidget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QVBoxLayout()
        self.button = qw.QPushButton('Save person')
        self.button.clicked.connect(self.save_button)
        self.button.setDisabled(True)

        self.name = qw.QLineEdit()
        self.name.setMaxLength(10)
        self.name.setPlaceholderText("Введите имя")
        self.name.textChanged.connect(self.name_changed)

        self.is_parent = qw.QCheckBox()
        self.is_parent.setText("is_parent")


        layout.addWidget(self.name)
        layout.addWidget(self.is_parent)
        layout.addWidget(self.button)

        self.setLayout(layout)



    def name_changed(self):
        if len(self.name.text()) > 0:
            self.button.setDisabled(False)
        else:
            self.button.setDisabled(True)

    def save_button(self):
        person = {
            'name': self.name.text(),
            'is_parent': self.is_parent.isChecked()
        }
        result = self.session.post('people/', json=person)
        print(result.text)