# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/draw/draw_link.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(377, 220)
        Dialog.setMinimumSize(QtCore.QSize(377, 220))
        Dialog.setMaximumSize(QtCore.QSize(377, 220))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 150, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(260, 150, 101, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 251, 51))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.Start_Point = QtWidgets.QComboBox(Dialog)
        self.Start_Point.setGeometry(QtCore.QRect(150, 180, 91, 25))
        self.Start_Point.setObjectName("Start_Point")
        self.End_Point = QtWidgets.QComboBox(Dialog)
        self.End_Point.setGeometry(QtCore.QRect(260, 180, 101, 25))
        self.End_Point.setObjectName("End_Point")
        self.Length = QtWidgets.QDoubleSpinBox(Dialog)
        self.Length.setGeometry(QtCore.QRect(30, 180, 91, 26))
        self.Length.setMinimum(0.01)
        self.Length.setProperty("value", 10.0)
        self.Length.setObjectName("Length")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 91, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 80, 211, 31))
        self.label_5.setObjectName("label_5")
        self.Link_num = QtWidgets.QTextBrowser(Dialog)
        self.Link_num.setGeometry(QtCore.QRect(30, 110, 211, 31))
        self.Link_num.setObjectName("Link_num")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Link"))
        self.label.setText(_translate("Dialog", "Start Point"))
        self.label_2.setText(_translate("Dialog", "End Point"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Setting two Points for the New Link.</span></p></body></html>"))
        self.Start_Point.setWhatsThis(_translate("Dialog", "Start point for next link."))
        self.End_Point.setWhatsThis(_translate("Dialog", "End point for next link."))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>Length</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>Link number</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

