#Andrew Patton
#Christopher Pillgreen
#Setup Instructions: Install Selenium and Pyside6 using the following commands:
#pip install selenium
#pip install PySide6

# Nov 30: Experimenting with amazon
# Dec 1: Simple Gui
# Dec 4: Created simple Amazon Scraper concept
# Dec 6: Added support for multiple formats on Amazon
# Dec 6: Experimented with builtin python threading
# Dec 7: Added Scraper ABC
# Dec 8: More Thread Experimentation
# Dec 8: Experimenting with Google Scraper
# Dec 10: Large Changes to UI and Design (adding loading and logo)
# Dec 11: Moved to QThreading
# Dec 12: Completed Million Class, Implemented Headless
# Dec 12: Unimplemented Google, Bug fixes and UI
# Dec 13: Finished Implementing Multithreaded Scraping

# Sources
# https://doc.qt.io/qtforpython-6/
# https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/


from PySide6.QtWidgets import QApplication, QMainWindow # UI handler
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QWidget # layout manipulation
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit # widgets
from PySide6.QtCore import QSize, Qt # sizing and alignment
from PySide6.QtCore import QRunnable, Slot, QThreadPool, QObject, Signal # managing threads
from PySide6.QtGui import QFont, QMovie, QPixmap # fonts, gifs, images
import Scraper # data module
from collections.abc import Callable # for reference (typehints), not for use

TITLE = QFont()
TITLE.setPointSize(75)
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

MAINTITLE = QFont()
MAINTITLE.setPointSize(40)
MAINTITLE.setFamily('Times New Roman')


class Worker(QRunnable):
    '''queues a function with an argument to be called in a new thread'''
    def __init__(self, toCall: Callable, arg, main: QMainWindow):
        super().__init__()
        self.toCall = toCall
        self.arg = arg
        self.signals = WorkerSignal()
        self.signals.finished.connect(main.signalRecieved)

    @Slot()
    def run(self):
        self.toCall(self.arg)
        self.signals.finished.emit()    

class WorkerSignal(QObject):
    '''notifies helper methods when a task is complete'''
    finished = Signal()

class StartWindow(QMainWindow):

    def __init__(self):
        '''initializes user interface'''
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

    def createTitleCard(self) -> QHBoxLayout:
        '''renders logo'''
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

    def createNavBar(self) -> QVBoxLayout:
        '''responsible for rendering search bar and button'''
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

    def setRelative(self, relative: QMainWindow):
        '''responsible for linking starting window to main window'''
        self.relative = relative

    def search(self):
        '''initiates search for books. (connected to search button)'''
        isbn = self.searchBar.text()
        if isbn:
            self.relative.show()
            self.hide()
            self.relative.startLoading(isbn)
        
class MainWindow(QMainWindow):
    tasks: list[Worker] = []
    signals = 0

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

    def runTasks(self):
        '''runs queued tasks'''
        for task in MainWindow.tasks:
            self.threadpool.start(task)

    def signalRecieved(self):
        '''tracks when tasks are completed'''
        MainWindow.signals += 1
        if MainWindow.signals == 4:
            MainWindow.signals = 0
            self.stopLoading()

    def _createTitleCard(self) -> QHBoxLayout:
        '''renders logo'''
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
        '''responsible for rendering search bar and button'''
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
        self.searchBar.returnPressed.connect(self.search)

        return navBar
    
    def _createHeader(self) -> QVBoxLayout:
        '''responsible for rendering header'''
        header = QVBoxLayout() 

        bookTitle = QLabel(Scraper.Scraper.title)
        bookTitle.setFont(MAINTITLE)
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
        '''responsible for rendering data'''
        stacks = QGridLayout()
        col = 0
        print(Scraper.Scraper.results)
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

    def startLoading(self, isbn: str | int):
        '''queues up and runs tasks and displays loading animation'''
        self.setFixedSize(QSize(300, 300))
        self.loading = QMovie('Project Resouces\\loading.gif')
        loadingContainer = QLabel()
        loadingContainer.setMovie(self.loading)
        self.setCentralWidget(loadingContainer)
        self.loading.start()
        MainWindow.tasks = []
        MainWindow.tasks.append(Worker(Scraper.Title, isbn, self))
        MainWindow.tasks.append(Worker(Scraper.Amazon, isbn, self))
        MainWindow.tasks.append(Worker(Scraper.Barnes, isbn, self))
        MainWindow.tasks.append(Worker(Scraper.Million, isbn, self))
        self.runTasks()

    def stopLoading(self):
        '''renders, resizes, and displays data on page'''
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
        '''initiates search for books. (connected to search button)'''
        isbn = self.searchBar.text()
        if isbn:
            self.startLoading(isbn)

if __name__ == '__main__':
    app = QApplication()

    start = StartWindow()
    main = MainWindow()

    start.setRelative(main)
    start.show()

    app.exec()

    # example isbns

    # 9780062024022
    # 9780199608522
    # 9781603095020
    # 9781603095174
    # 9781603095273
