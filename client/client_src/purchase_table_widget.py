from custom_session import BasedSession
import PyQt6.QtWidgets as qw
import PyQt6.QtGui as qg
import PyQt6.QtCore as qc

class CalendarSignals(qc.QObject):
    date_finalized = qc.pyqtSignal()

class MyCalendar(qw.QCalendarWidget):

    def __init__(self):
        super().__init__()
        self.begin_date = None
        self.end_date = None

        self.highlight_format = qg.QTextCharFormat()
        self.highlight_format.setBackground(qg.QBrush(qc.Qt.GlobalColor.blue))
        # sself.highlight_format.setBackground(qg.QPalette.highlight())
        # self.highlight_format.setForeground(qg.QPalette.highlightedText())

        self.signals = CalendarSignals()

        self.selectionChanged.connect(self.date_is_clicked)
        print(super().dateTextFormat())

    def format_range(self, format):
        if self.begin_date and self.end_date:
            d0 = min(self.begin_date, self.end_date)
            d1 = max(self.begin_date, self.end_date)
            while d0 <= d1:
                self.setDateTextFormat(d0, format)
                d0 = d0.addDays(1)

    def date_is_clicked(self):
        # reset highlighting of previously selected date range
        date = self.selectedDate()

        print('nya')
        self.format_range(qg.QTextCharFormat())
        if qw.QApplication.keyboardModifiers() & qc.Qt.KeyboardModifier.ShiftModifier and self.begin_date:
            self.end_date = date
            print('with shift')
            # set highilighting of currently selected date range
            self.format_range(self.highlight_format)
        else:
            self.begin_date = date
            self.end_date = None

        if self.end_date and self.begin_date:
            if self.end_date < self.begin_date:
                self.begin_date, self.end_date = self.end_date, self.begin_date

        self.signals.date_finalized.emit()

# class ButtonSignals(qc.QObject):
#     advanced_clicked = qc.pyqtSignal(int, int, int)

class MyButtonWidget(qw.QPushButton):
    def __init__(self, text, purchase_id, position):
        super().__init__(text)

        self.purchase_id = purchase_id
        self.position = position
        print('position = ', self.position.y())

        self.clicked.connect(self.was_clicked)

    def was_clicked(self):
        print(self.purchase_id)
        context = qw.QMenu(self)
        context.addAction(qg.QAction("test 1", self))
        context.addAction(qg.QAction("test 2", self))
        context.addAction(qg.QAction("test 3", self))
        context.exec(self.pos() + self.position)



class PurchaseTableWitdget(qw.QWidget):
    def __init__(self, session: BasedSession):
        super().__init__()
        self.session = session

        layout = qw.QGridLayout()

        self.table = qw.QTableWidget(self)
        self.table.setRowCount(10)
        self.table.setColumnCount(4)

        all_purchases = session.get('/purchases?expand=true').json()
        self.table.setHorizontalHeaderLabels(["дата", "сумма", "покупатель", "действие"])

        layout.addWidget(self.table, 1, 0, 2, 2)

        for idx, elem in enumerate(all_purchases):
            self.table.setItem(idx, 0, qw.QTableWidgetItem(elem['purchase_date']))
            self.table.setItem(idx, 1, qw.QTableWidgetItem(str(elem['amount'])))
            self.table.setItem(idx, 2, qw.QTableWidgetItem(elem['buyer']['name']))
            action_button = MyButtonWidget('...', elem['purchase_id'], self.table.pos())
            self.table.setCellWidget(idx, 3, action_button)

            # action_button.clicked.connect(self.actions_for_purchase)

        self.calendar = MyCalendar()
        layout.addWidget(self.calendar, 0, 0)
        self.calendar.signals.date_finalized.connect(self.date_changed)

        print(self.calendar.begin_date, self.calendar.end_date)
        self.setLayout(layout)


    def date_changed(self):
        print(self.calendar.begin_date)
        print(self.calendar.end_date)

        params = {
            'expand': True
        }

        if self.calendar.begin_date:
            params['start_date'] = self.calendar.begin_date.toString(format=qc.Qt.DateFormat.ISODate)

        if self.calendar.end_date:
            params['end_date'] = self.calendar.end_date.toString(format=qc.Qt.DateFormat.ISODate)

        if self.calendar.begin_date and not self.calendar.end_date:
            params['end_date'] = params['start_date']

        all_purchases = self.session.get('/purchases', params=params).json()
        print(all_purchases)
        self.table.clearContents()
        for idx, elem in enumerate(all_purchases):
            self.table.setItem(idx, 0, qw.QTableWidgetItem(    elem['purchase_date'] ))
            self.table.setItem(idx, 1, qw.QTableWidgetItem(str(elem['amount'       ])))
            self.table.setItem(idx, 2, qw.QTableWidgetItem(    elem['buyer']['name'] ))
