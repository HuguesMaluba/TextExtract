import os
import sys
from fpdf import FPDF
from PyQt5 import QtCore, QtWidgets,QtGui
import cv2
import pytesseract
from ui_loading import  Ui_SplashScreen
from ui_main import  Ui_MainWindow
compteur = 0

#fenetre principale
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.fileName = None
        self.fileExtrat = None
        self.textImg = None
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        #enlever la bar de titre
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.setupUi(self)
        self.ui.btnExit.clicked.connect(self.close)
        self.ui.btnSelect.clicked.connect(self.selectFile)
        self.ui.btnExtract.clicked.connect(self.extractText)
        self.ui.btnFile.clicked.connect(self.pdfFile)

    def pdfFile(self):
        
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save The text to PDF File","","PDF Files (*.pdf)", options=options)
        if fileName and self.textImg != None:
            pdf = FPDF()
  
            pdf.add_page()
                
            pdf.set_font("Arial", size = 15)
                
            pdf.cell(200, 10, txt = self.textImg, ln = 1, align = 'C')
                
            pdf.output(fileName) 
                
            if  self.fileExtrat != None: 
                os.remove(self.fileExtrat)
                
            self.fileExtrat = None
            self.fileName = None
            self.textImg = None 
            #self.ui.labelExtract.clear()
            #self.ui.imgSelect.clear()
                
    
    def selectFile(self):
        if self.fileExtrat != None:
            self.ui.labelExtract.clear()
            self.fileExtrat = None
            os.remove(self.fileExtrat)

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select Image File", "","All Files (*)", options=options)
        if fileName:
            self.ui.imgSelect.setPixmap(QtGui.QPixmap(fileName))
            self.ui.imgSelect.setScaledContents(True)
            self.fileName = fileName

    def extractText(self):
        
        if self.fileName != None:
            img = cv2.imread(self.fileName)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            dataFile = self.fileName.split(".")
            self.fileExtrat = 'extract.'+dataFile[-1]
            #dimenson de l'image
            hImg,wImg,_= img.shape

            #detection des caracteres
            boxes = pytesseract.image_to_boxes(img)
            self.textImg =  pytesseract.image_to_string(img)
            for box in boxes.splitlines():
                box = box.split(" ")
                character = box[0]
                x = int(box[1])
                y = int(box[2])
                x2 = int(box[3])
                y2 = int(box[4])
                cv2.rectangle(img, (x, hImg - y), (x2, hImg - y2), (0, 255, 0), 1)
                cv2.imwrite(self.fileExtrat , cv2.putText(img, character, (x, hImg -y2), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255) , 1))
            
            self.ui.labelExtract.setPixmap(QtGui.QPixmap(self.fileExtrat))
            self.ui.labelExtract.setScaledContents(True)
            self.extractImg = "extract.png"
        
        
            
            
            
#fenetre de demarrage
class LoadingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        
        #enlever la bar de titre
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        #shadow effet
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setYOffset(0)
        self.shadow.setXOffset(0)
        self.shadow.setColor(QtGui.QColor(0,0,0,60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        
        self.timer.start(35)
        self.show()
    
    def progress(self):
        global compteur
        #affecter une valeur a la bar de progresson
        self.ui.progressBar.setValue(compteur)
        if compteur > 100:
            #arreter le temps
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            compteur +=1
            
        
        
if "__main__" == __name__:
    app = QtWidgets.QApplication(sys.argv)
    window = LoadingWindow()
    sys.exit(app.exec_())