# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/simulate/set_rod.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(377, 289)
        Dialog.setMinimumSize(QtCore.QSize(377, 289))
        Dialog.setMaximumSize(QtCore.QSize(377, 289))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 220, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 220, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 251, 51))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.Start = QtWidgets.QComboBox(Dialog)
        self.Start.setGeometry(QtCore.QRect(30, 250, 101, 25))
        self.Start.setObjectName("Start")
        self.End = QtWidgets.QComboBox(Dialog)
        self.End.setGeometry(QtCore.QRect(250, 250, 101, 25))
        self.End.setObjectName("End")
        self.Start_Angle = QtWidgets.QDoubleSpinBox(Dialog)
        self.Start_Angle.setGeometry(QtCore.QRect(30, 180, 91, 26))
        self.Start_Angle.setMinimum(0.01)
        self.Start_Angle.setMaximum(360.0)
        self.Start_Angle.setProperty("value", 0.01)
        self.Start_Angle.setObjectName("Start_Angle")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 80, 131, 21))
        self.label_5.setObjectName("label_5")
        self.Rod_num = QtWidgets.QTextBrowser(Dialog)
        self.Rod_num.setGeometry(QtCore.QRect(30, 110, 211, 31))
        self.Rod_num.setObjectName("Rod_num")
        self.End_Angle = QtWidgets.QDoubleSpinBox(Dialog)
        self.End_Angle.setGeometry(QtCore.QRect(250, 180, 91, 26))
        self.End_Angle.setMinimum(0.01)
        self.End_Angle.setMaximum(100000.0)
        self.End_Angle.setProperty("value", 50.0)
        self.End_Angle.setObjectName("End_Angle")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(110, 190, 151, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(120, 161, 131, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.buttonBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.Start.raise_()
        self.End.raise_()
        self.label_5.raise_()
        self.Rod_num.raise_()
        self.line.raise_()
        self.End_Angle.raise_()
        self.Start_Angle.raise_()
        self.label_4.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Piston / Spring"))
        self.label.setText(_translate("Dialog", "Start point"))
        self.label_2.setText(_translate("Dialog", "End point"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Setting two Points for the New Rod.</span></p></body></html>"))
        self.Start.setWhatsThis(_translate("Dialog", "Start point for next link."))
        self.End.setWhatsThis(_translate("Dialog", "End point for next link."))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>New Rod number</p></body></html>"))
        self.label_4.setText(_translate("Dialog", "Length limit"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

