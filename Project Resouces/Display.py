#Andrew Patton
#Christopher Pillgreen
#Setup Instructions: Install Selenium and Pyside6 using the following commands
#pip install selenium
#pip install PySide6
from PySide6.QtWidgets import QApplication, QMainWindow # UI handler
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QWidget # layout manipulation
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit # widgets
from PySide6.QtCore import QSize, Qt # sizing and alignment
from PySide6.QtCore import QRunnable, Slot, QThreadPool, QObject, Signal # managing threads
from PySide6.QtGui import QFont, QMovie, QPixmap # fonts, gifs, images
import Scraper # data class
from collections.abc import Callable # for reference, not used

TITLE = QFont()
TITLE.setPointSize(40)
TITLE.setFamily('Times New Roman')

SUBTITLE = QFont()
SUBTITLE.setPointSize(20)
SUBTITLE.setFamily('Times New Roman')

SUB = QFont()
SUB.setPointSize(15)
SUB.setFamily('Times New Roman')

BOOKFINDER = QFont()
BOOKFINDER.setPointSize(22)
BOOKFINDER.setFamily('Times New Roman')


class Worker(QRunnable):

    def __init__(self, toCall, arg):
        self.toCall = toCall
        self.arg = arg
        self.signalz = WorkerSignal()


    @Slot
    def run(self):
        self.toCall(self.arg)
        self.signalz.finished.emit()    

class WorkerSignal(QObject):
    finished = Signal()

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

        self.searchBar.returnPressed.connect(self.search)

        return subInterface

    def setRelative(self, relative: 'MainWindow'):
        self.relative = relative

    def search(self):
        self.relative.show()
        self.hide()
        self.relative.startLoading(self.searchBar.text())
        
class MainWindow(QMainWindow):
    tasks: list[Worker] = []

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

    def runTasks(self):
        for task in MainWindow.tasks:
            task.signalz.finished.connect(self.signalRecieved)
            self.threadpool.start(task)

    def signalRecieved(self):
        MainWindow.signals += 1
        if MainWindow.signals == 4:
            MainWindow.signals = 0
            self.stopLoading()

    def _createTitleCard(self) -> QHBoxLayout:
        titleCard = QHBoxLayout()

        image = QPixmap('Project Resouces\\bookStackIcon.png')
        image = image.scaledToWidth(50)
        imageContainer = QLabel()
        imageContainer.setPixmap(image)
        titleCard.addWidget(imageContainer)
    
        programName = QLabel('Book Finder')
        programName.setFixedWidth(150)
        programName.setFont(BOOKFINDER)
        titleCard.addWidget(programName)

        return titleCard
    
    def _createNavBar(self) -> QHBoxLayout:
        navBar = QHBoxLayout()

        self.searchBar = QLineEdit()

        self.searchBar.setPlaceholderText('Please enter an ISBN Number')
        self.searchBar.setFont(SUB)
        self.searchBar.setFixedSize(QSize(650, 50))

        searchButton = QPushButton('Search')
        searchButton.setFont(SUB)
        searchButton.clicked.connect(self.search)

        
        searchButton.setFixedSize(100, 55)

        titleCard = self._createTitleCard()
        navBar.addLayout(titleCard)
        navBar.addWidget(self.searchBar)
        navBar.addWidget(searchButton)
        navBar.addSpacerItem(QSpacerItem(0, 50))

        return navBar
    
    def _createHeader(self) -> QHBoxLayout:
        header = QVBoxLayout() 

        bookTitle = QLabel(Scraper.Scraper.title)
        bookTitle.setFont(TITLE)
        bookTitle.setAlignment(Qt.AlignCenter)
        header.addWidget(bookTitle)

        subHeader = QGridLayout()
        venders = 'Amazon-Barnes & Noble-Books a Million'.split('-')
        
        index = 0
        for vender in venders:
            index += 1
            venderHead = QLabel(vender)
            venderHead.setFont(SUBTITLE)
            venderHead.setFixedSize(QSize(333, 100))
            venderHead.setAlignment(Qt.AlignCenter)
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
                formatLabel.setAlignment(Qt.AlignCenter)
                stacks.addWidget(formatLabel, row, col)
                row += 1
            col += 1
        
        stacks.setAlignment(Qt.AlignCenter)
        stacksLayout = QHBoxLayout()
        stacksLayout.addLayout(stacks)

        return stacksLayout

    def startLoading(self, isbn):
        self.setFixedSize(QSize(300, 300))
        self.loading = QMovie('Project Resouces\\loading.gif')
        loadingContainer = QLabel()
        loadingContainer.setMovie(self.loading)
        self.setCentralWidget(loadingContainer)
        self.loading.start()

        MainWindow.tasks.append(Worker(Scraper.Amazon, isbn))
        MainWindow.tasks.append(Worker(Scraper.Barnes, isbn))
        MainWindow.tasks.append(Worker(Scraper.Million, isbn))
        manager.finished.connect(self.stopLoading)#####################

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
        isbn = self.searchBar.text()
        self.startLoading(isbn)

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
    main.show()
    start.setRelative(main)

    switch = Toggle(main)
    switch.show()

    app.exec()
    # 9780062024022
    # 9780199608522