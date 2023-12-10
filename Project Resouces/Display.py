#Andrew Patton
#Christopher Pillgreen
from PySide6.QtWidgets import QApplication, QMainWindow # UI handler
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget # layout manipulation
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit # widgets
from PySide6.QtCore import QSize #misc
from PySide6.QtGui import QFont, QMovie, QPixmap # fonts, gifs, images
from Scraper import Scraper # retrieve data

titleFont = QFont()
titleFont.setPointSize(75)
titleFont.setFamily('Garamond')

subTitleFont = QFont()
subTitleFont.setPointSize(20)
subTitleFont.setFamily('Garamond')

subFont = QFont()
subFont.setPointSize(15)
subFont.setFamily('Garamond')

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
        programName.setFont(titleFont)
        titleCard.addWidget(programName)
        return titleCard

    def createNavBar(self):
        subInterface = QVBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Please enter an ISBN Number")
        self.searchBar.setFont(subTitleFont)
        subInterface.addWidget(self.searchBar)

        searchButton = QPushButton('Search')
        searchButton.setFont(subTitleFont)
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
        image = image.scaledToHeight(30)
        imageContainer = QLabel()
        imageContainer.setPixmap(image)
        titleCard.addWidget(imageContainer)
    
        programName = QLabel('Book Finder')
        programName.setFont(subFont)
        titleCard.addWidget(programName)
        return titleCard
    
    def createNavBar(self) -> QHBoxLayout:
        navBar = QHBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Please enter an ISBN Number')
        self.searchBar.setFont(subFont)
        self.searchBar.setFixedSize(QSize(250, 30))

        searchButton = QPushButton('Search')
        searchButton.setFont(subFont)
        searchButton.setFixedSize(75, 35)

        titleCard = self._createTitleCard()
        navBar.addLayout(titleCard)
        navBar.addWidget(self.searchBar)
        navBar.addWidget(searchButton)
        navBar.addSpacerItem(QSpacerItem(300, 35))

        return navBar
    
    def createHeader(self) -> QHBoxLayout:
        header = QHBoxLayout()
        header.addSpacerItem(QSpacerItem(50, 35))
        venders = 'Amazon-Barnes&Nobel-Books a Million-Google'.split('-')
        for vender in venders:
            venderHead = QLabel(vender)
            venderHead.setFont(subTitleFont)
            header.addWidget(venderHead)
        header.addSpacerItem(QSpacerItem(50, 35))
        header.setSpacing(50)
        return header

    def createStacks(self) -> QHBoxLayout:
        stacks = QHBoxLayout()
        stacks.addSpacerItem(QSpacerItem(50, 50))
        for vender in Scraper.results.keys():
            column = QVBoxLayout()
            for item in Scraper.results[vender]:
                container = QHBoxLayout()

                formatLabel = QLabel(item[0])
                formatLabel.setFont(subFont)
                formatLabel.setFixedSize(100, 25) 
                container.addWidget(formatLabel)

                priceLabel = QLabel(str(item[1]))
                priceLabel.setFont(subFont)  
                priceLabel.setFixedSize(100, 25) 
                container.addWidget(priceLabel)

                column.addLayout(container)
            stacks.addLayout(column)
        stacks.addSpacerItem(QSpacerItem(50, 50))
        return stacks

    def startLoading(self, isbn):
        self.setFixedSize(QSize(300, 300))
        self.loading = QMovie('Project Resouces\\loading.gif')
        loadingContainer = QLabel()
        loadingContainer.setMovie(self.loading)
        self.setCentralWidget(loadingContainer)
        self.loading.start()

    def stopLoading(self):
        self.loading.stop()
        self.setFixedSize(775, 500)
        mainInterface = QVBoxLayout()
        mainInterface.addLayout(self.createNavBar())
        mainInterface.addLayout(self.createHeader())
        mainInterface.addLayout(self.createStacks())
        widget = QWidget()
        widget.setLayout(mainInterface)
        self.setCentralWidget(widget)

    def search(self):
        pass

'''
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
'''

if __name__ == '__main__':
    app = QApplication()

    main = MainWindow()

    start = StartWindow()
    start.setRelative(main)
    start.show()

    app.exec()