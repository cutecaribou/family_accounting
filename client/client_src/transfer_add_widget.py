from custom_session import BasedSession
import PyQt6.QtWidgets as qw
import sys

class AddNewTransferWidget(qw.QWidget):
    def __init__(self, session: BasedSession, purchase_id: int = None):
        super().__init__()
        self.session = session
        self.purchase_id = purchase_id

        layout = qw.QHBoxLayout()
        self.button = qw.QPushButton('Save transfer')
        self.button.setDisabled(True)

        self.sender_box = qw.QComboBox()
        self.receiver_box = qw.QComboBox()
        self.id_to_idx = {}
        self.fill_cmbx()

        if self.purchase_id is not None:
            self.fill_receiver_from_purchase()
            self.receiver_box.setDisabled(True)

        self.receiver_box.currentIndexChanged.connect(self.print_current_selection)
        self.sender_box.currentIndexChanged.connect(self.print_current_selection)

        self.amount = qw.QSpinBox()
        self.amount.setMaximum(1000000000)
        self.amount.valueChanged.connect(self.amount_changed)

        layout.addWidget(self.sender_box)
        layout.addWidget(self.receiver_box)
        layout.addWidget(self.amount)
        layout.addWidget(self.button)

        self.setLayout(layout)


    def fill_cmbx(self):
        all_users = self.session.get('people/').json()
        for elem in all_users:
            if elem['is_parent']:
                self.receiver_box.addItem(elem['name'], userData=elem)
                self.id_to_idx[elem['person_id']] = self.receiver_box.count() - 1
            else:
                self.sender_box.addItem(elem['name'], userData=elem)
                self.id_to_idx[elem['person_id']] = self.receiver_box.count() - 1

    def amount_changed(self):
        if self.amount.value() > 0:
            self.button.setDisabled(False)
        else:
            self.button.setDisabled(True)

    def print_current_selection(self):
        print(self.sender_box.currentData())
        print(self.receiver_box.currentData())
        print('-' * 80)

    def fill_receiver_from_purchase(self):
        purchase = self.session.get(f'purchases/{self.purchase_id}').json()
        receiver_id = purchase['buyer_id']
        receiver_idx_in_cmbx = self.id_to_idx[receiver_id]
        self.receiver_box.setCurrentIndex(receiver_idx_in_cmbx)
        # print('покупка: ', purchase)

        # self.receiver_box.addItem(receiver['name'], userData=receiver)

