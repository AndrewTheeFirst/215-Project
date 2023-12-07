#Andrew Patton
#Christopher Pillgreen
from Scraper import Amazon
from PySide6.QtWidgets import \
     QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QAbstractItemView, QMessageBox, QWidget, QListWidget
from Scraper import main, Amazon
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Finder")
        self.resize(300,40)

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Please enter an ISBN Number")
        layout.addWidget(self.input)
        

        addButton = SearchButton('Search', self)
        addButton.clicked.connect(self.on_enter_clicked)  
        layout.addWidget(addButton)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.input.returnPressed.connect(self.on_enter_clicked)

    def on_enter_clicked(self):
        entered_text = self.input.text()
        QMessageBox.information(self, f"{entered_text}", "Book Prices Here")

class SearchButton(QPushButton):
    def __init__(self, text: str, parentWindow: MainWindow):
        super().__init__(text)
        self.parentWindow = parentWindow
        self.clicked.connect(self.onClick)

    def onClick(self):
        print('test')
        isbn = self.parentWindow.input.text()
        Amazon(isbn)
        for thread in Amazon.threads:
            thread.start()
        for thread in Amazon.threads:
            thread.join()
    pass
if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

    