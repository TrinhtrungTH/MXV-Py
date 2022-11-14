# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import  sys
from PyQt5 import QtGui, QtWidgets
from Controlers import Controler
import logging
from datetime import datetime as dt
import string

def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Controler.main()
    ex.show()
    sys.exit(app.exec_())
    #logger.info('Finished')
if __name__ == '__main__':
    main()
