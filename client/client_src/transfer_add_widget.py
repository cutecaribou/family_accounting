from custom_session import BasedSession
import PyQt6.QtWidgets as qw
import sys

class AddNewTransferWidget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QHBoxLayout()
        self.button = qw.QPushButton('Save transfer')
        self.button.setDisabled(True)
        # self.button.clicked.connect(self.save_button)

        self.box1 = qw.QComboBox()
        self.box2 = qw.QComboBox()
        self.box1.currentIndexChanged.connect(self.print_current_selection)
        self.box2.currentIndexChanged.connect(self.print_current_selection)

        self.line = qw.QSpinBox()
        self.line.setMaximum(1000000000)
        self.line.valueChanged.connect(self.amount_changed)

        layout.addWidget(self.box1)
        layout.addWidget(self.box2)
        layout.addWidget(self.line)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.fill_cmbx()

    def fill_cmbx(self):
        all_users = self.session.get('people/').json()
        for elem in all_users:
            if elem['is_parent']:
                self.box2.addItem(elem['name'], userData=elem)
            else:
                self.box1.addItem(elem['name'], userData=elem)

    def amount_changed(self):
        if self.line.value() > 0:
            self.button.setDisabled(False)
        else:
            self.button.setDisabled(True)

    def print_current_selection(self):
        print(self.box1.currentData())
        print(self.box2.currentData())
        print('-' * 80)
