from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidgetItem

class perubahan:   
    def change(self):
        selected_date = self.calendarWidget.selectedDate().toPyDate().strftime('%d-%m-%Y')
        self.listWidget.clear()
        self.cursor.execute('SELECT * FROM tasks WHERE date=?', (selected_date,))
        rows = self.cursor.fetchall()
        for row in rows:
            task = f"{row[0]} - {row[1]}"
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)