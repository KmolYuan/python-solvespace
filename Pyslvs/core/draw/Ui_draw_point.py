# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/draw/draw_point.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(377, 219)
        Dialog.setMinimumSize(QtCore.QSize(377, 219))
        Dialog.setMaximumSize(QtCore.QSize(377, 219))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/point.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.X_coordinate = QtWidgets.QDoubleSpinBox(Dialog)
        self.X_coordinate.setGeometry(QtCore.QRect(40, 180, 81, 26))
        self.X_coordinate.setMinimum(-10000.0)
        self.X_coordinate.setMaximum(10000.0)
        self.X_coordinate.setObjectName("X_coordinate")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 150, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 150, 81, 21))
        self.label_2.setObjectName("label_2")
        self.Y_coordinate = QtWidgets.QDoubleSpinBox(Dialog)
        self.Y_coordinate.setGeometry(QtCore.QRect(140, 180, 81, 26))
        self.Y_coordinate.setMinimum(-10000.0)
        self.Y_coordinate.setMaximum(10000.0)
        self.Y_coordinate.setObjectName("Y_coordinate")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 241, 51))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.Fix_Point = QtWidgets.QCheckBox(Dialog)
        self.Fix_Point.setGeometry(QtCore.QRect(260, 180, 101, 21))
        self.Fix_Point.setObjectName("Fix_Point")
        self.Point_num = QtWidgets.QTextBrowser(Dialog)
        self.Point_num.setGeometry(QtCore.QRect(40, 110, 241, 31))
        self.Point_num.setObjectName("Point_num")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 80, 101, 21))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Point"))
        self.X_coordinate.setWhatsThis(_translate("Dialog", "X coordinate for next point."))
        self.label.setText(_translate("Dialog", "x coordinate"))
        self.label_2.setText(_translate("Dialog", "y coordinate"))
        self.Y_coordinate.setWhatsThis(_translate("Dialog", "Y coordinate for next point."))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Setting Coordinates for the New Point.</span></p></body></html>"))
        self.Fix_Point.setText(_translate("Dialog", "&Fixed"))
        self.Point_num.setWhatsThis(_translate("Dialog", "Name for next point."))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>Point Number</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

