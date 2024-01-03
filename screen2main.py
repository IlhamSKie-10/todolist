import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import QTime
from plyer import notification
from screen1 import TodoApp1

import sqlite3


Ui_MainWindow, QMainWindowBase = uic.loadUiType("UI2.ui")

class TodoApp2(QMainWindow, Ui_MainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)  
        self.setWindowTitle('To Do List')
        self.setGeometry(100, 100, 845, 390)
        self.stacked_widget = stacked_widget  
        self.initUI()

    def initUI(self):
        self.calendarWidget.selectionChanged.connect(self.change)
        
        # Tombol add
        self.add.clicked.connect(self.updatetask)
        self.time_edit.setTime(QTime.currentTime())
        self.lineEdit.clear()
        
        #tombol save change
        self.save.clicked.connect(self.savechange)
        #tombol delete 
        self.delete_2.clicked.connect(self.deletetask)

        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                                 (task text, time text, date text)''')

        self.retrieve_tasks()

    def savechange(self):
        
        items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]

        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()

        for item_text in items:
            task, time = item_text.split(' - ')
            date = self.calendarWidget.selectedDate().toPyDate().strftime('%d-%m-%Y')
            self.cursor.execute('INSERT INTO tasks VALUES (?, ?, ?)', (task, time, date))
            self.conn.commit()

        self.close()

        # Kembali ke window sebelumnya (misalnya, window utama)
        self.previous_window = TodoApp1(self.stacked_widget)
        self.previous_window.show()

    def switch_to_screen1(self):
        self.stacked_widget.setCurrentIndex(0)

    def deletetask(self):
        selected_items = self.listWidget.selectedItems()

        for item in selected_items:
            text = item.text()
            task, time = text.split(' - ')

            self.cursor.execute('DELETE FROM tasks WHERE task=? AND time=?', (task, time))
            self.conn.commit()

        for item in selected_items:
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
        
    def retrieve_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        for row in rows:
            task = f"{row[0]} - {row[1]}"
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

    def updatetask(self):
        if self.lineEdit.text():
            task = self.lineEdit.text()
            time = self.time_edit.time().toString("hh:mm")
            date = self.calendarWidget.selectedDate().toPyDate().strftime('%d-%m-%Y')
            todo = f"{task} - {time}"
            item = QListWidgetItem(todo)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

            self.cursor.execute('INSERT INTO tasks VALUES (?, ?, ?)', (task, time, date))
            self.conn.commit()

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

    def showNotification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    todo_app = TodoApp2(widget)
    todo_app.show()
    sys.exit(app.exec_())
