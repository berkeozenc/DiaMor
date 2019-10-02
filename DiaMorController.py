import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import os


from DiaMorModel import DiaMorModel
from DiaMorView import DiaMorView


class DiaMorController:

    def run(self):
        app = QApplication(sys.argv)
        self.createDummy = False
        self.view = DiaMorView()
        self.connectViewActions()
        self.model = DiaMorModel()
        sys.exit(app.exec_())

    def connectViewActions(self):
        self.view.openProjectMenuBtn.triggered.connect(self.openProject)
        self.view.saveProjectMenuBtn.triggered.connect(self.save)
        self.view.twolFileList_ListWidgetModel.itemChanged.connect(self.twolListAction)
        self.view.xml_button.clicked.connect(self.selectXml)
        self.view.lexiconFile_button.clicked.connect(self.selectWords)
        self.view.generate_Button.clicked.connect(self.generateAction)
        self.view.twolRefresh_button.clicked.connect(self.refreshTwolList)

    def openProject(self):
        self.model.projectPath = str(self.view.showDirectoryDialog())
        self.view.projectPath_label.setText(self.model.projectPath)
        fileList = os.listdir(self.model.projectPath)
        if "project.conf" in fileList:
            self.load()
            self.view.generate_Button.setEnabled(True)
            return
        noTwol = True
        for f in fileList:
            if ".twol" in f:
                noTwol = False
                self.model.twolFileNameList.append((2, f))
                self.view.addToTwolList(f, 2)
        if noTwol:
            self.view.twolFileList_Label.setText("No .twol file found. Dummy.twol is created")
            self.createDummy = True
            self.model.writeDummyTwol()
            self.model.twolFileNameList.append((2, "dummy.twol"))
            self.view.addToTwolList("dummy.twol", 2)

    def selectXml(self):
        if self.model.projectPath != "":
            fname = self.view.showFileDialog(self.model.projectPath, "*.xml")
            if fname[0] != "":
                path_elements = fname[0].split("/")
                self.view.xml_lineEdit.setText(path_elements[len(path_elements)-1])
                self.model.xmlFileName = path_elements[len(path_elements)-1]
                self.view.generate_Button.setEnabled(True)
        else:
            self.view.showWarning("Please select a project folder.")

    def selectWords(self):
        if self.model.projectPath != "":
            fname = self.view.showFileDialog(self.model.projectPath, "*.txt")
            if fname[0] != "":
                path_elements = fname[0].split("/")
                self.view.lexiconFile_lineEdit.setText(path_elements[len(path_elements)-1])
                self.model.lexiconFileName = path_elements[len(path_elements)-1]
                self.view.generate_Button.setEnabled(True)
        else:
            self.view.showWarning("Please select a project folder.")

    def readNewTwolOrder(self):
        self.model.twolFileNameList.clear()
        for i in range(0, self.view.twolFileList_ListWidgetModel.rowCount()):
            item = self.view.twolFileList_ListWidgetModel.item(i)
            state = item.checkState()
            self.model.twolFileNameList.append((state, item.text()))

    def twolListAction(self):
        QTimer.singleShot(1, self.readNewTwolOrder)

    def save(self):
        if self.model.projectPath != "":
            self.model.save()
            self.view.showWarning("Project saved.")

    def load(self):
        try:
            self.model.load()
            self.view.xml_lineEdit.setText(self.model.xmlFileName)
            self.view.lexiconFile_lineEdit.setText(self.model.lexiconFileName)
            for twol in self.model.twolFileNameList:
                self.view.addToTwolList(twol[1], int(twol[0]))
        except:
            self.view.showWarning("Loading Failed.")


    def generateAction(self):

        self.model.generateAlphabet()
        self.model.xml2lexc()
        if self.createDummy:
            self.model.writeDummyTwol()
        self.model.writeMakeFile()
        self.view.showWarning("Generation completed.")

    def refreshTwolList(self):
        fileList = os.listdir(self.model.projectPath)
        self.view.clearTwolList()
        self.model.clearTwolList()
        noTwol = True
        for f in fileList:
            if f != "dummy.twol" and ".twol" in f:
                noTwol = False
                self.model.twolFileNameList.append((2, f))
                self.view.addToTwolList(f, 2)
        if noTwol:
            self.view.twolFileList_Label.setText("No .twol file found. Dummy.twol is created")
            self.createDummy = True
            # self.model.writeDummyTwol()
            self.model.twolFileNameList.append((2, "dummy.twol"))
            self.view.addToTwolList("dummy.twol", 2)
        else:
            self.view.twolFileList_Label.setText("Found .twol files")







DiaMorController().run()