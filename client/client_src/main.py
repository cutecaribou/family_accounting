from custom_session import BasedSession
import json
from models import Person, PersonWithID
import PyQt6.QtWidgets as qw
import sys
from PyQt6.QtGui import QColor, QPalette


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


class AddNewTransferWidget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QHBoxLayout()
        button = qw.QPushButton('Save transfer')

        self.parent_list = []
        self.child_list = []

        self.box1 = qw.QComboBox()
        self.box2 = qw.QComboBox()
        self.box1.currentIndexChanged.connect(self.print_current_selection)
        self.box2.currentIndexChanged.connect(self.print_current_selection)
        line = qw.QSpinBox()
        line.setMaximum(1000000000)

        layout.addWidget(self.box1)
        layout.addWidget(self.box2)
        layout.addWidget(line)
        layout.addWidget(button)

        self.setLayout(layout)
        self.fill_cmbx()

    def fill_cmbx(self):
        all_users = self.session.get('people/').json()
        for elem in all_users:
            if elem['is_parent']:
                self.box2.addItem(elem['name'])
                self.parent_list.append(elem)
            else:
                self.box1.addItem(elem['name'])
                self.child_list.append(elem)

    def print_current_selection(self):
        if self.child_list and self.parent_list:
            print(self.child_list[self.box1.currentIndex()])
            print(self.parent_list[self.box2.currentIndex()])
            print('-' * 80)

class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = BasedSession('http://localhost:8000/')
        self.setWindowTitle("My App")

        # self.layout = qw.QVBoxLayout()
        # self.setLayout(self.layout)

        tabs = qw.QTabWidget()
        tabs.setTabPosition(qw.QTabWidget.TabPosition.North)

        button_table = Color('red')
        # self.button_table.clicked.connect(self.activate_tab_1)

        add_line_button = AddNewTransferWidget(self.session)

        tabs.addTab(button_table, "Табличка?")
        tabs.addTab(add_line_button, "Добавить запись")

        self.setCentralWidget(tabs)

    # def activate_tab_1(self):
    #     self.stacklayout.setCurrentIndex(0)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
#     test()
