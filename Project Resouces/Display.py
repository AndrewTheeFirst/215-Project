#Andrew Patton
#Christopher Pillgreen
#Setup Instructions: Install Selenium and Pyside6 using the following commands
#pip install selenium
#pip install PySide6
from PySide6.QtWidgets import QApplication, QMainWindow # UI handler
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QWidget # layout manipulation
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit # widgets
from PySide6.QtCore import QSize, Qt # sizing and alignment
from PySide6.QtCore import QRunnable, QObject, QThreadPool, Signal, QThread # managing threads
from PySide6.QtGui import QFont, QMovie, QPixmap # fonts, gifs, images
import Scraper # data class

TITLE = QFont()
TITLE.setPointSize(75)
TITLE.setFamily('Garamond')

SUBTITLE = QFont()
SUBTITLE.setPointSize(20)
SUBTITLE.setFamily('Garamond')

SUB = QFont()
SUB.setPointSize(15)
SUB.setFamily('Garamond')

class WorkerSignal():
    pass

class Worker(QObject):
    def __init__(self, isbn):
        super().__init__()
        self.isbn = isbn

    def task(self):
        Scraper.Scraper.run(self.isbn)

class Manager(QThread):

    def run(self, isbn):
        worker = Worker(isbn)
        worker.task()

class StartWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(650, 300))

        mainInterface = QVBoxLayout()

        titleCard = self.createTitleCard()
        subInterface = self.createNavBar()

        mainInterface.addLayout(titleCard)
        mainInterface.addLayout(subInterface)

        widget = QWidget()
        widget.setLayout(mainInterface)
        self.setCentralWidget(widget)

    def createTitleCard(self):
        titleCard = QHBoxLayout()

        image = QPixmap('Project Resouces\\bookStackIcon.png')
        image = image.scaledToHeight(75)
        imageContainer = QLabel()
        imageContainer.setPixmap(image)
        titleCard.addWidget(imageContainer)
    
        programName = QLabel('Book Finder')
        programName.setFont(TITLE)
        titleCard.addWidget(programName)
        return titleCard

    def createNavBar(self):
        subInterface = QVBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Please enter an ISBN Number")
        self.searchBar.setFont(SUBTITLE)
        subInterface.addWidget(self.searchBar)

        searchButton = QPushButton('Search')
        searchButton.setFont(SUBTITLE)
        searchButton.clicked.connect(self.search)
        subInterface.addWidget(searchButton)

        return subInterface

    def setRelative(self, relative: 'MainWindow'):
        self.relative = relative

    def search(self):
        self.relative.show()
        self.hide()
        self.relative.startLoading(self.searchBar.text())
        
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def _createTitleCard(self) -> QHBoxLayout:
        titleCard = QHBoxLayout()

        image = QPixmap('Project Resouces\\bookStackIcon.png')
        image = image.scaledToWidth(50)
        imageContainer = QLabel()
        imageContainer.setPixmap(image)
        titleCard.addWidget(imageContainer)
    
        programName = QLabel('Book Finder')
        programName.setFixedWidth(150)
        programName.setFont(SUB)
        titleCard.addWidget(programName)

        return titleCard
    
    def _createNavBar(self) -> QHBoxLayout:
        navBar = QHBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Please enter an ISBN Number')
        self.searchBar.setFont(SUB)
        self.searchBar.setFixedSize(QSize(200, 50))

        searchButton = QPushButton('Search')
        searchButton.setFont(SUB)
        searchButton.setFixedSize(100, 55)

        titleCard = self._createTitleCard()
        navBar.addLayout(titleCard)
        navBar.addWidget(self.searchBar)
        navBar.addWidget(searchButton)
        navBar.addSpacerItem(QSpacerItem(600, 50))

        return navBar
    
    def _createHeader(self) -> QHBoxLayout:
        header = QVBoxLayout() 

        bookTitle = QLabel(Scraper.Scraper.title)
        bookTitle.setFont(TITLE)
        bookTitle.setAlignment(Qt.AlignCenter)
        header.addWidget(bookTitle)

        subHeader = QGridLayout()
        venders = 'Amazon-Barnes&Nobel-Books a Million'.split('-')
        
        index = 0
        for vender in venders:
            index += 1
            venderHead = QLabel(vender)
            venderHead.setFont(SUBTITLE)
            venderHead.setFixedSize(QSize(333, 100))
            venderHead.setAlignment(Qt.AlignLeft)
            subHeader.addWidget(venderHead, 1, index)

        header.addLayout(subHeader)
        
        return header

    def _createStacks(self) -> QHBoxLayout:
        stacks = QGridLayout()
        col = 0
        for vender in Scraper.Scraper.results.keys():
            row = 0
            for item in Scraper.Scraper.results[vender]:
                formatLabel = QLabel(f'{item[0]}: {item[1]}')
                formatLabel.setFont(SUB)
                formatLabel.setFixedWidth(333)
                formatLabel.setAlignment(Qt.AlignLeft)
                stacks.addWidget(formatLabel, row, col)
                row += 1
            col += 1
        return stacks

    def startLoading(self, isbn):
        self.setFixedSize(QSize(300, 300))
        self.loading = QMovie('Project Resouces\\loading.gif')
        loadingContainer = QLabel()
        loadingContainer.setMovie(self.loading)
        self.setCentralWidget(loadingContainer)
        self.loading.start()
        manager = Manager()
        manager.run(isbn)
        manager.finished.connect(self.stopLoading)

    def stopLoading(self): #########init of window##########
        self.loading.stop()
        self.setFixedSize(1000, 500)
        mainInterface = QVBoxLayout()
        mainInterface.addLayout(self._createNavBar())
        mainInterface.addLayout(self._createHeader())
        mainInterface.addLayout(self._createStacks())
        widget = QWidget()
        widget.setLayout(mainInterface)
        self.setCentralWidget(widget)

    def search(self):
        pass

class Toggle(QMainWindow):
    def __init__(self, main: MainWindow):
        super().__init__()
        layout = QVBoxLayout()

        self.main = main

        onButton = QPushButton('on')
        onButton.clicked.connect(self.on)
        layout.addWidget(onButton)

        offButton = QPushButton('off')
        offButton.clicked.connect(self.off)
        layout.addWidget(offButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on(self):
        self.main.startLoading()

    def off(self):
        self.main.stopLoading()

if __name__ == '__main__':
    app = QApplication()

    start = StartWindow()
    start.show()

    main = MainWindow()
    start.setRelative(main)

    switch = Toggle(main)
    switch.show()

    app.exec()
    # 9780062024022
    # 9780199608522