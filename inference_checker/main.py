import sys
import os
import json
import pandas as pd
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui


class MyWindow(QMainWindow):
    def __init__(self, root="dataset", json="test.json", inference="submission.csv"):
        super().__init__()

        
        self.root = root
        self.json = json
        self.inference = inference

        self.current = 0
        self.length = 0
        self.images = self.loadJson()
        self.inference = None
        self.color = [QtCore.Qt.white, QtCore.Qt.red, QtCore.Qt.green, 
                    QtCore.Qt.blue, QtCore.Qt.yellow, QtCore.Qt.magenta,
                     QtCore.Qt.cyan, QtCore.Qt.black, QtCore.Qt.darkRed,
                      QtCore.Qt.darkGreen]
        self.classes = ["General trash", "Paper", "Paper pack", "Metal", 
                    "Glass", "Plastic", "Styrofoam", "Plastic bag", "Battery", "Clothing"]
        self.initUI()

    def loadJson(self):
        json_file = None
        with open(os.path.join(self.root, self.json), 'r') as f:
            json_file = json.load(f)
            self.length = len(json_file["images"]) - 1
        return json_file["images"]
    
    def initUI(self):
        # menu bar
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open submission.csv file')
        openFile.triggered.connect(self.openDialog)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        menu = menubar.addMenu('&Menu')
        menu.addAction(openFile)
        menu.addAction(exitAction)

        # label
        self.imageLabel = QLabel('image')
        self.imageLabel.setStyleSheet("background-color: #ffffff")
        # self.imageLabel.resize(720, 720)
        self.imageLabel.setText("temp")
        self.pixmap = QtGui.QPixmap(os.path.join(self.root, self.images[self.current]["file_name"])).scaledToWidth(720)
        self.imageLabel.setPixmap(self.pixmap)


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

        labelHbox = QHBoxLayout()
        labelHbox.addStretch(1)
        labelHbox.addWidget(self.imageLabel)
        labelHbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(5)
        vbox.addLayout(labelHbox)
        vbox.addStretch(5)
        vbox.addLayout(buttonHbox)
        vbox.addStretch(1)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(vbox)

        # window
        self.setWindowTitle("Inference Checker v1.0")
        self.setGeometry(1280, 1280, 1024, 1024)
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
            fileName = self.images[self.current]["file_name"]
            self.pixmap = QtGui.QPixmap(os.path.join(self.root, fileName))

            if self.inference is not None:
                try:

                    pred = self.inference.loc[self.inference['image_id'] == fileName]["PredictionString"].item().split()
                    predDic = []
                    for i in range(0, len(pred), 6):
                        info = {}
                        info["class"] = pred[i]
                        info["conf"] = pred[i+1]
                        info["bbox"] = [pred[i+2], pred[i+3], pred[i+4], pred[i+5]]
                        predDic.append(info)

                    painterInstance = QtGui.QPainter(self.pixmap)
                    penRectangle = QtGui.QPen(QtCore.Qt.red)
                    penRectangle.setWidth(5)
                    print('total predit:', len(predDic), fileName)
                    for dic in predDic:
            
                        penRectangle.setColor(self.color[int(dic["class"])])
                        painterInstance.setPen(penRectangle)
                        x, y = float(dic["bbox"][0]), float(dic["bbox"][1])
                        width = float(dic["bbox"][2]) - float(dic["bbox"][0])
                        height = float(dic["bbox"][3])- float(dic["bbox"][1])
                        painterInstance.drawRect(x, y, width, height)
                        painterInstance.setFont(QtGui.QFont('Arial', 24))
                        painterInstance.drawText(x+5, y+20, self.classes[int(dic["class"])])
                        
                        time.sleep(.05)

                    painterInstance.end()
                except:
                    print("There is no prediction")
            self.pixmap = self.pixmap.scaledToWidth(720)
            self.imageLabel.setPixmap(self.pixmap)

    def eventPrevious(self):
        if self.current > 0:
            self.current -= 1
            fileName = self.images[self.current]["file_name"]
            self.pixmap = QtGui.QPixmap(os.path.join(self.root, fileName))

            if self.inference is not None:
                try:
                    pred = self.inference.loc[self.inference['image_id'] == fileName]["PredictionString"].item().split()
                    predDic = []
                    for i in range(0, len(pred), 6):
                        info = {}
                        info["class"] = pred[i]
                        info["conf"] = pred[i+1]
                        info["bbox"] = [pred[i+2], pred[i+3], pred[i+4], pred[i+5]]
                        predDic.append(info)

                    painterInstance = QtGui.QPainter(self.pixmap)
                    penRectangle = QtGui.QPen(QtCore.Qt.red)
                    penRectangle.setWidth(5)
                    print('total predit:', len(predDic), fileName)
                    for dic in predDic:
            
                        penRectangle.setColor(self.color[int(dic["class"])])
                        painterInstance.setPen(penRectangle)
                        x, y = float(dic["bbox"][0]), float(dic["bbox"][1])
                        width = float(dic["bbox"][2]) - float(dic["bbox"][0])
                        height = float(dic["bbox"][3])- float(dic["bbox"][1])
                        painterInstance.drawRect(x, y, width, height)
                        painterInstance.setFont(QtGui.QFont('Arial', 24))
                        painterInstance.drawText(x+5, y+20, self.classes[int(dic["class"])])
                        
                        time.sleep(.05)

                    painterInstance.end()
                except:
                    print("There is no prediction")
            self.pixmap = self.pixmap.scaledToWidth(720)
            self.imageLabel.setPixmap(self.pixmap)

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.inference = pd.read_csv(fname[0])
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Left:
            self.eventPrevious()
        elif e.key() == QtCore.Qt.Key_Right:
            self.eventNext()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())