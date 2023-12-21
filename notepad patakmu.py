import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
from PyQt5.QtGui import QKeySequence


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if not self.is_empty():
            return self.items[-1]


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.undo_stack = Stack()
        self.redo_stack = Stack()

        self.initUI()

    def initUI(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Menubar dasaran
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')

        # Open act
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        # Save act
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        # Exit act
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Undo act
        undo_action = QAction('Undo', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)

        # Redo act
        redo_action = QAction('Redo', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad SAT!!')
        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
                self.clearStacks()

    def saveFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())
                self.clearStacks()

    def undo(self):
        current_text = self.text_edit.toPlainText()
        self.redo_stack.push(current_text)

        if not self.undo_stack.is_empty():
            undo_text = self.undo_stack.pop()
            self.text_edit.setPlainText(undo_text)

    def redo(self):
        current_text = self.text_edit.toPlainText()
        self.undo_stack.push(current_text)

        if not self.redo_stack.is_empty():
            redo_text = self.redo_stack.pop()
            self.text_edit.setPlainText(redo_text)

    def clearStacks(self):
        self.undo_stack = Stack()
        self.redo_stack = Stack()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad_app = NotepadApp()
    sys.exit(app.exec_())
