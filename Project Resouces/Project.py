#Andrew Patton
#Christopher Pillgreen

from PySide6.QtWidgets import \
     QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QAbstractItemView, QMessageBox, QWidget, QListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Finder")
        self.resize(300,40)

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Please enter an ISBN Number")
        layout.addWidget(self.input)

        addButton = QPushButton("Enter")
        addButton.clicked.connect(self.on_enter_clicked)  
        layout.addWidget(addButton)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.input.returnPressed.connect(self.on_enter_clicked)

    def on_enter_clicked(self):
        entered_text = self.input.text()
        QMessageBox.information(self, f"Book Title Here{entered_text}", "Book Prices Here")
        
if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()