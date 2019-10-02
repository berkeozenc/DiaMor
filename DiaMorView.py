from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QLineEdit, QListWidget,
                             QListWidgetItem, QAbstractItemView, QLabel, QCheckBox, QMessageBox, QListView, QPushButton)
import platform



class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class DiaMorView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        system = platform.system()

        self.projectPath_label = QLabel(self)
        self.projectPath_label.setText("Select a project folder")
        self.projectPath_label.move(22, 30)
        self.projectPath_label.resize(400, 30)

        self.xml_lineEdit = ClickableLineEdit(self)
        self.xml_lineEdit.move(20, 70)
        self.xml_lineEdit.resize(400,30)
        self.xml_lineEdit.setPlaceholderText("Choose xml file")
        self.xml_lineEdit.setReadOnly(True)

        self.xml_button = QPushButton(self)
        self.xml_button.move(430, 74)
        self.xml_button.resize(20,20)
        icon = QIcon()
        icon.addPixmap(QPixmap("assets/folder.png"))
        self.xml_button.setIcon(icon)
        self.xml_button.setIconSize(QSize(20,20))

        self.lexiconFile_lineEdit = ClickableLineEdit(self)
        self.lexiconFile_lineEdit.move(20, 110)
        self.lexiconFile_lineEdit.resize(400, 30)
        #self.lexiconFile_lineEdit.clicked.connect(self.showFileSelection)
        self.lexiconFile_lineEdit.setPlaceholderText("Choose lexicon file")
        self.lexiconFile_lineEdit.setReadOnly(True)

        self.lexiconFile_button = QPushButton(self)
        self.lexiconFile_button.move(430, 114)
        self.lexiconFile_button.resize(20, 20)
        icon = QIcon()
        icon.addPixmap(QPixmap("assets/folder.png"))
        self.lexiconFile_button.setIcon(icon)
        self.lexiconFile_button.setIconSize(QSize(20, 20))

        self.twolFileList_Label = QLabel(self)
        self.twolFileList_Label.setText("Found .twol files: ")
        self.twolFileList_Label.move(22, 160)
        self.twolFileList_Label.resize(400, 30)

        self.twolRefresh_button = QPushButton("Refresh", self)
        self.twolRefresh_button.move(350, 160)

        self.twolFileList_ListWidget = QListView(self)
        self.twolFileList_ListWidgetModel = QStandardItemModel(self.twolFileList_ListWidget)
        self.twolFileList_ListWidget.setModel(self.twolFileList_ListWidgetModel)
        self.twolFileList_ListWidget.move(20, 200)
        self.twolFileList_ListWidget.resize(430, 300)
        self.twolFileList_ListWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.twolFileList_ListWidget.show()
        #self.twolFileList_ListWidget.selectionModel().selectionChanged.connect(self.t)

        self.generate_Button = QPushButton("Generate", self)
        self.generate_Button.move(350, 510)
        self.generate_Button.setEnabled(False)

        if system == "Darwin":
            self.projectPath_label.move(22, 10)
            self.xml_lineEdit.move(20, 50)
            self.xml_button.move(430, 54)
            self.lexiconFile_lineEdit.move(20, 90)
            self.lexiconFile_button.move(430, 94)
            self.twolFileList_Label.move(22, 140)
            self.twolRefresh_button.move(350, 140)
            self.twolFileList_ListWidget.move(20, 180)
            self.generate_Button.move(350, 490)






        self.statusBar()
        #openFile.setShortcut('Ctrl+O')
        #createProjectMenuBtn.triggered.connect(self.createProject)
        self.openProjectMenuBtn = QAction('Open', self)
        self.openProjectMenuBtn.setShortcut('Ctrl+O')
        self.openProjectMenuBtn.setStatusTip('Open existing project')
        self.saveProjectMenuBtn = QAction('Save', self)
        self.saveProjectMenuBtn.setShortcut('Ctrl+S')
        self.saveProjectMenuBtn.setStatusTip('Save existing project')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Project')
        fileMenu.addAction(self.openProjectMenuBtn)
        fileMenu.addAction(self.saveProjectMenuBtn)

        self.setGeometry(50, 50, 470, 550)
        self.setWindowTitle('DiaMor')
        self.show()

    def t(self):
        print("order changed")

    def showWarning(self, message):
        QMessageBox.about(self, "Warning", message)

    def showDirectoryDialog(self):
        return QFileDialog.getExistingDirectory(self, "Select Directory")

    def showFileDialog(self, path, fileType):
        return QFileDialog.getOpenFileName(self, 'Open file', path, fileType)

    def clearTwolList(self):
        self.twolFileList_ListWidgetModel.clear()

    def addToTwolList(self, fileName, state):
        item = QStandardItem(fileName)
        item.setCheckable(True)
        item.setCheckState(state)
        item.setEditable(False)
        item.setDropEnabled(False)
        self.twolFileList_ListWidgetModel.appendRow(item)
        '''
        item = QListWidgetItem(self.twolFileList_ListWidget)
        item.setText(fileName)
        self.twolFileList_ListWidget.addItem(item)
        cb = QCheckBox()
        self.twolFileList_ListWidget.setItemWidget(item, cb)
        '''




