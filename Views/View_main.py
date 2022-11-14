from PyQt5 import QtGui,QtCore,QtWidgets
from Views import frmMain

class View_main(QtWidgets.QMainWindow,frmMain.Ui_MainWindow):
    clicked = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(View_main, self).__init__(parent)
        self.initEvent()

    def initEvent(self):
        self.btnAutoman.clicked.connect( self.btnAutoman_clicked)

    def btnAutoman_clicked(self):
        bAutomode = True