from custom_session import BasedSession
import json
from models import Person, PersonWithID
import PyQt6.QtWidgets as qw
import sys
from PyQt6.QtGui import QColor, QPalette
from person_add_widget import AddNewPersonWidget
from transfer_add_widget import  AddNewTransferWidget
from purchase_add_widget import AddNewPurchaseWidget
from purchase_table_widget import PurchaseTableWitdget


def test():
    base_url = 'http://localhost:8000/'

    session   = BasedSession(base_url)
    all_users = session.get('people/').json()

    print(json.dumps(all_users, indent = 4, ensure_ascii=False))

    person = Person(
        name = 'Test',
        is_parent = True
    )

    result = session.post('people/', json=person.model_dump())
    print(result.text)

    all_users = session.get('people/').json()

    print(json.dumps(all_users, indent = 4, ensure_ascii=False))

    for person in all_users:
        if person['name'] == 'Test':
            session.delete('people/' + str(person['person_id']))



class Color(qw.QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = BasedSession('http://localhost:8000/')
        self.setWindowTitle("My App")

        # self.layout = qw.QVBoxLayout()
        # self.setLayout(self.layout)

        tabs = qw.QTabWidget()
        tabs.setTabPosition(qw.QTabWidget.TabPosition.North)

        button_table = PurchaseTableWitdget(self.session)
        # self.button_table.clicked.connect(self.activate_tab_1)

        add_line_button = AddNewTransferWidget(self.session)
        add_person_button = AddNewPersonWidget(self.session)
        add_purchase_button = AddNewPurchaseWidget(self.session)

        tabs.addTab(button_table, "Табличка?")
        tabs.addTab(add_person_button, "Добавить человека")
        tabs.addTab(add_purchase_button, "Добавить покупку")
        tabs.addTab(add_line_button, "Добавить перевод")
        self.setCentralWidget(tabs)

    # def activate_tab_1(self):
    #     self.stacklayout.setCurrentIndex(0)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
#     test()
