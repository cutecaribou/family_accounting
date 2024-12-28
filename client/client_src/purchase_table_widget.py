from custom_session import BasedSession
import PyQt6.QtWidgets as qw
from PyQt6.QtCore import QDate, Qt


class PurchaseTableWitdget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QHBoxLayout()

        self.table = qw.QTableWidget(self)
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["покупатель", "сумма", "дата"])


        all_purchases = session.get('/purchases').json()

        for idx, elem in enumerate(all_purchases):
            # print(idx,  elem)
            self.table.setItem(idx, 0, qw.QTableWidgetItem(elem['purchase_date']))
            self.table.setItem(idx, 1, qw.QTableWidgetItem(str(elem['amount'])))
            # self.table.setItem(idx, 0, qw.QTableWidgetItem(elem['name']))

        layout.addWidget(self.table)
