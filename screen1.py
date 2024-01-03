import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import QtWidgets, uic
from notif import notifi





Ui_MainWindow1, QMainWindowBase1 = uic.loadUiType("UI1.ui")

class TodoApp1(QMainWindow, Ui_MainWindow1):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('To Do List')
        self.setGeometry(100, 100, 600, 390)
        self.stacked_widget = stacked_widget
        self.done.clicked.connect(self.donefunc)
        self.miss.clicked.connect(self.missfunc)
        self.notyet.clicked.connect(self.notyetfunct)

    def switch_to_screen2(self):
        # Create instance TodoApp2 and add it to the stacked widget
        screen2 = TodoApp2(self.stacked_widget)
        self.stacked_widget.addWidget(screen2)
        # Set current index to the index of screen2
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(screen2))

    def donefunc(self):
        notifnya = notifi()
        self.donefunc.selectionChanged.connect(notifnya.showNotification)
        
    def missfunc(self):
        pass
    
    def notyetfunct(self):
        pass



def switch_to_screen1():
    stacked_widget = QStackedWidget()
    screen1 = TodoApp1(stacked_widget)
    stacked_widget.addWidget(screen1)
    stacked_widget.setCurrentIndex(stacked_widget.indexOf(screen1))
    return stacked_widget  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    stacked_widget = switch_to_screen1()
    window.setCentralWidget(stacked_widget)
    window.show()  
    sys.exit(app.exec_())
