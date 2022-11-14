
import sys
import os
import time
import platform
import numpy as np
import pandas as pandas
import cv2
import  logging
from PyQt5 import QtGui,QtCore,QtWidgets
from Views import frmMain
from datetime import datetime as dt

class Controler_main(QtWidgets.QMainWindow,frmMain.Ui_MainWindow):
    now = dt.now()
    time = now.strftime("%Y-%b-%d_%H-%M-%S")
    logName = 'Log/MXV_Py_{0}{1}'.format(time, ".log")
    logging.basicConfig(filename=logName,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w'
                        )
    logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    # # Test messages
    # logger.debug("Harmless debug Message")
    # logger.info("Just an information")
    # logger.warning("Its a Warning")
    # logger.error("Did you try to divide by zero")
    # logger.critical("Internet is down")
    #logger.info('Started')


    logger =logging.getLogger()
    logger.info("Start main controller")


    clicked = QtCore.pyqtSignal(float, float)
    def __init__(self, parent = None):
        print("Starting ")
        super(Controler_main, self).__init__(parent)
        self.initValue()
        self.initUI()
        self.initEvent()
        self.logger.info("init finish")
    def initValue(self):

        global Cam, Camenable
        self.scaleFactor = 0.0
        self.fileName = ""
        self.setAcceptDrops(True)
        self.dragstart = None
        self.bAutomode = False
        self.saveimg = 0
       # Se
        print("init value finihish")
        self.logger.info("initValue finish")
    def initUI(self):
        #print("init value finihish2")
        self.setupUi(self)
        self.__Version__ = '0.0.0.0'
        txtTitle = 'MXV-PyCv: {4} | Ver: {0} | CamNum: {1} | PrmFile: {2} | SpecFile: {3}' \
                   ''.format(self.__Version__,
                             "001",
                             "1234",
                             "2212",
                             "2222")
        self.setWindowTitle(txtTitle)
        self._textStatus = ''
        self.logger.info("initUI finish")

    def initEvent(self):
        #print("init value finihish3")
        #self.btnAutoman.clicked(self.btnAutoman_clicked)
        self.btnAutoman.clicked.connect(self.btnAutoman_clicked)
        self.btnTakePhoto.clicked.connect(self.btnTakePhoto_clicked)
        self.actionClear_msg.triggered.connect(self.Clear_msg_trigger)
        self.action_Open.triggered.connect(self.OpenImg)
        self.action_Exit.triggered.connect(self.close_application)
        #self.

        self.logger.info("initEvent finish")

    def btnAutoman_clicked(self):
        if self.bAutomode == True:
            self.bAutomode = False
            self.btnAutoman.setStyleSheet("color: Black; background-color: white ")
            self.btnAutoman.setText("Manual")
            #print(" manual")
        elif self.bAutomode == False:
            self.bAutomode = True
            self.btnAutoman.setStyleSheet("color: Black ; background-color: green ")
            self.btnAutoman.setText("Auto")
           # print("Automode")
    def btnTakePhoto_clicked(self):
        self.btnTakePhoto.setEnabled(False)
        imgReturn = cv2.imread("Template\Masster.bmp")
        if self.bAutomode== False:
            try:
                options = QtWidgets.QFileDialog.Options()
                # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                                    'Images (*.png *.jpeg *.jpg *.bmp *.gif)',                                                                    options=options)

                imgread = cv2.imread(fileName)
                if (imgread.shape[1]  >1 ):
                    #print("image was reed successfully ")
                    self.Update_msg("image was read successfully")
                    self.Update_msg("image file: {0}".format(fileName))
                    imgReturn = imgread.copy()
                    if (self.saveimg == 0):
                     self.save_image(imgReturn)


                # else:
                # if 1:
                #     img = self.imgread.copy()
                #     scale_percent = 30  # percent of original size
                #     width = int(img.shape[1] * scale_percent / 100)
                #     height = int(img.shape[0] * scale_percent / 100)
                #     dim = (width, height)
                #     img2 = cv2.resize(self.imgSrc0, dim, interpolation = cv2.INTER_AREA)
                #     # cv2.imshow("Testimg",img2)
                #     # cv2.waitKey(0)
                #     # cv2.destroyAllwindows()
                   #  cv2.destroyAllWindows()

            except:
                    self.Update_msg( "img read fail")
                    self.btnTakePhoto.setEnabled(True)
                    self.logger.error("img read fail")
        elif self.bAutomode == True:
            imgReturn =  cv2.imread("2021114_155617.bmp")

            cv2.imshow("Test img-auto",imgReturn)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.Update_msg("takepic done")
            if (self.saveimg == 0):
                self.save_image(imgReturn)


        self.btnTakePhoto.setEnabled(True)
        return imgReturn
    def OpenImg(self):
        self.btnTakePhoto.setEnabled(False)
        imgReturn = cv2.imread("Template\Masster.bmp")
        if self.bAutomode== False:
            try:
                options = QtWidgets.QFileDialog.Options()
                # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                                    'Images (*.png *.jpeg *.jpg *.bmp *.gif)',
                                                                    options=options)

                imgread = cv2.imread(fileName)
                if (imgread.shape[1]  >1 ):
                    #print("image was reed successfully ")
                    self.Update_msg("image was read successfully")
                    self.Update_msg("image file: {0}".format(fileName))

                    imgReturn = imgread.copy()
            except:
                self.Update_msg("img read fail")
                self.btnTakePhoto.setEnabled(True)
                self.logger.error("img read fail")
        self.btnTakePhoto.setEnabled(True)

        _rest,disImage = self.mat2qtshow(imgReturn)
        self.lblDisplayImage.setPixmap(disImage)
        self.scrollArea.setVisible(True)
        self.scrollArea.setWidgetResizable(True)
        self.lblDisplayImage.adjustSize()

        return imgReturn

    def Update_msg(self, msg):
        self.lbMsg.appendPlainText(msg)
        self.logger.info(msg)
    def Clear_msg_trigger(self):
        self.lbMsg.clear()
    def save_image(self,imgSrc):
        t = time.localtime()
        name = './Image/{0}{1}{2}_{3}{4}{5}.bmp'.format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        cv2.imwrite(name, imgSrc)
    def mat2qtshow(self,imgMat):
        _ret = False
        pixmap = None
        try:
            h,w,c = imgMat.shape
            bytesPerLine = 3 * w
            qImg = QtGui.QImage(imgMat.data, w, h, bytesPerLine,
                                QtGui.QImage.Format_RGB888)

            pixmap = QtGui.QPixmap(qImg)
            _ret = True
        except:
            _ret = False
        return _ret, pixmap
    def Imageproceesing (self ):

        try:
            test = True


        except:
            self.Update_msg("image processing fail ")
    def normalSize(self):
        self.lblDisplayImage.adjustSize()
        self.scaleFactor = 1.0
        self.scaleDisplay = (self.lblDisplayImage.size().width(), self.lblDisplayImage.size().height())
        self.imgMouse = cv2.resize(self.imgDisplay, self.scaleDisplay)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.lblDisplayImage.resize(self.scaleFactor * self.lblDisplayImage.pixmap().size())
        #h, w, a = self.imgSrc0.shape
        self.scaleDisplay = (self.lblDisplayImage.size().width(), self.lblDisplayImage.size().height())
        self.imgMouse = cv2.resize(self.imgDisplay, self.scaleDisplay)
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))






    def close_application(self):
        print("Close application ")
        self.Update_msg("Exit application ")
        sys.exit()


def main():
    print(" Controler_main running ")
    app = QtWidgets.QApplication(sys.argv)
    ex = Controler_main()
    ex.show()
    sys.exit(app.exec_())

