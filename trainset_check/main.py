import sys
import os
import json
import pandas as pd
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

data_root = '../dataset/'
annotaion = '../dataset/train.json'

class MyWindow(QMainWindow):
    def __init__(self, root="../dataset/", json="train.json"):
        super().__init__()

        
        self.root = root
        self.json = json

        self.current = -1
        self.length = 0
        self.images, self.annotations = self.loadJson()

        self.color = [QtCore.Qt.white, QtCore.Qt.red, QtCore.Qt.green, 
                    QtCore.Qt.blue, QtCore.Qt.yellow, QtCore.Qt.magenta,
                     QtCore.Qt.cyan, QtCore.Qt.black, QtCore.Qt.darkRed,
                      QtCore.Qt.darkGreen]

        self.colorText = ["white", "red", "green", "blue", "yellow","magenta","cyan", "black","darkRed","darkGreen"]
        self.classes = ["General trash", "Paper", "Paper pack", "Metal", 
                    "Glass", "Plastic", "Styrofoam", "Plastic bag", "Battery", "Clothing"]

        self.initUI()
    
    def loadJson(self):
        json_file = None
        with open(os.path.join(self.root, self.json), 'r') as f:
            json_file = json.load(f)
            self.length = len(json_file["images"]) - 1

        annotations = json_file['annotations']
        annotations_list = [[] for _ in range(self.length + 1)]
        
        for ann in annotations:
            annotations_list[int(ann["image_id"])].append(ann)

        return json_file["images"], annotations_list
    
    def initUI(self):
        # menu bar
        # openFile = QAction('Open', self)
        # openFile.setShortcut('Ctrl+O')
        # openFile.setStatusTip('Open submission.csv file')
        # openFile.triggered.connect(self.openDialog)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        menu = menubar.addMenu('&Menu')
        # menu.addAction(openFile)
        menu.addAction(exitAction)

        # label
        self.imageLabel = QLabel('image')
        #self.imageLabel.setStyleSheet("background-color: #ffffff")
        # self.imageLabel.resize(720, 720)
        self.imageLabel.setText("Inference tool for Boostcamp")
        #self.pixmap = QtGui.QPixmap(os.path.join(self.root, self.images[self.current]["file_name"])).scaledToWidth(720)
        #self.imageLabel.setPixmap(self.pixmap)


        # button
        nextButton = QPushButton('next')
        nextButton.clicked.connect(self.eventNext)
        previousButton = QPushButton('previous')
        previousButton.clicked.connect(self.eventPrevious)

        # layout
        buttonHbox = QHBoxLayout()
        buttonHbox.addStretch(1)
        buttonHbox.addWidget(previousButton)
        buttonHbox.addWidget(nextButton)
        buttonHbox.addStretch(1)

        legendVbox = QVBoxLayout()

        for i in range(len(self.classes)):
            label = QLabel(self.classes[i])
            label.setText(self.classes[i])
            fontColor = "color : balck;" if self.colorText[i] == "white" else "color : white;"
            label.setStyleSheet(
                fontColor+
                f"background-color: {self.colorText[i]};"
            )
            legendVbox.addWidget(label)
            
        labelHbox = QHBoxLayout()
        
        labelHbox.addStretch(1)
        labelHbox.addLayout(legendVbox)
        labelHbox.addWidget(self.imageLabel)
        labelHbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(labelHbox)
        vbox.addStretch(5)
        vbox.addLayout(buttonHbox)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(vbox)

        # window
        self.setWindowTitle("Inference Checker v1.0")
        self.setGeometry(1024, 1024, 1280, 1280)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def eventNext(self):
        if self.current < self.length:
            self.current += 1
            fileName = self.images[self.current]["file_name"] # images에 current 번째 id의 파일 이름
            self.pixmap = QtGui.QPixmap(os.path.join(self.root, fileName))

            predictions = self.annotations[self.current]

            print("current image id:", self.current)

            painterInstance = QtGui.QPainter(self.pixmap)
            penRectangle = QtGui.QPen(QtCore.Qt.red)
            penRectangle.setWidth(3)

            for pre in predictions:
                category_id = pre["category_id"]
                bbox = list(map(float, pre["bbox"]))
                print(category_id, bbox)
                penRectangle.setColor(self.color[int(category_id)])
                painterInstance.setPen(penRectangle)

                painterInstance.drawRect(bbox[0], bbox[1], bbox[2], bbox[3])
                time.sleep(.05)

            painterInstance.end()
            
            self.pixmap = self.pixmap.scaledToWidth(650)
            self.imageLabel.setPixmap(self.pixmap)

    def eventPrevious(self):
        if self.current > 0:
            self.current -= 1
            fileName = self.images[self.current]["file_name"]
            self.pixmap = QtGui.QPixmap(os.path.join(self.root, fileName))
            

            predictions = self.annotations[self.current]

            print("current image id:", self.current)

            painterInstance = QtGui.QPainter(self.pixmap)
            penRectangle = QtGui.QPen(QtCore.Qt.red)
            penRectangle.setWidth(3)

            for pre in predictions:
                category_id = pre["category_id"]
                bbox = list(map(float, pre["bbox"]))
                print(category_id, bbox)
                penRectangle.setColor(self.color[int(category_id)])
                painterInstance.setPen(penRectangle)

                painterInstance.drawRect(bbox[0], bbox[1], bbox[2], bbox[3])
                time.sleep(.05)

            painterInstance.end()

            self.pixmap = self.pixmap.scaledToWidth(650)
            self.imageLabel.setPixmap(self.pixmap)

    # def openDialog(self):
    #     fname = QFileDialog.getOpenFileName(self, 'Open file', './')
    #     if fname[0]:
    #         self.inference = pd.read_csv(fname[0])
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_A:
            self.eventPrevious()
        elif e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_D:
            self.eventNext()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())