import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QVBoxLayout, QTimeEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, QTime
from plyer import notification
import qdarkstyle

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('To Do List')
        #self.setWindowIcon(QtGui.QIcon("PATH LOGOMU"))
        self.initUI()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def initUI(self):
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Masukan task anda disini")

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.addTask)

        self.delete_button = QPushButton("Delete Task") 
        self.delete_button.clicked.connect(self.deleteTask)

        self.clearall_button = QPushButton("Clear All") 
        self.clearall_button.clicked.connect(self.clearAll)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Task', 'Deadline'])

        layout = QVBoxLayout(self)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.clearall_button)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.table)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def addTask(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

        task = self.line_edit.text()
        deadline = self.time_edit.time().toString("HH:mm")

        # ambil yang ada di QlineEdit,taroh ke tabel 
        task_item = QTableWidgetItem(task)
        deadline_item = QTableWidgetItem(deadline)
        self.table.setItem(rowPosition, 0, task_item)
        self.table.setItem(rowPosition, 1, deadline_item)
        
        #notifnya
        notif_title = "To Do List"
        notif_message = f"Tugas baru ditambahkan: {task} (Deadline: {deadline})"
        self.showNotification(notif_title, notif_message)
        
    def deleteTask(self):
        #kalo ini, dihapus buat yang diseelect kusor aja y
        selected_rows = set(index.row() for index in self.table.selectionModel().selectedRows())

        #ini buat hapusnya,jadi dia akan disortir secara terbalik/reverse(tabel akan dihapus dari bawah ke atas/ besar ke kecil menurut nomer colom)
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)

    def clearAll(self):
        #hapus semua, setRowCount 0, buat nyetel Row table menjadi 0 kak
        self.table.setRowCount(0)
    
    def showNotification(self, title, message):
        notification.notify(
            title = title,
            message = message,
            timeout = 10
        )
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
