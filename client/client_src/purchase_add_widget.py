from custom_session import BasedSession
import PyQt6.QtWidgets as qw
from PyQt6.QtCore import QDate, Qt
import sys


class AddNewPurchaseWidget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QHBoxLayout()
        self.button = qw.QPushButton('Save purchase')
        self.button.setDisabled(True)
        self.button.clicked.connect(self.save_button)

        self.calendar = qw.QCalendarWidget()
        self.calendar.setGridVisible(True)

        self.amount = qw.QSpinBox()
        self.amount.setMaximum(1000000000)
        self.amount.valueChanged.connect(self.amount_changed)

        self.box = qw.QComboBox()
        self.fill_cmbx()

        layout.addWidget(self.calendar)
        layout.addWidget(self.amount)
        layout.addWidget(self.box)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def fill_cmbx(self):
        all_users = self.session.get('people/').json()
        for elem in all_users:
            if elem['is_parent']:
                self.box.addItem(elem['name'], userData=elem)
            else:
                self.box.addItem(elem['name'], userData=elem)

    def amount_changed(self):
        if self.amount.value() > 0:
            self.button.setDisabled(False)
        else:
            self.button.setDisabled(True)


    def save_button(self):
        person_id = self.box.currentData()['person_id']
        purchase = {
            'purchase_date': self.calendar.selectedDate().toString(format=Qt.DateFormat.ISODate),
            'amount': self.amount.value(),
            'buyer_id': person_id
        }
        result = self.session.post('purchases/', json=purchase)
        print(result.text)