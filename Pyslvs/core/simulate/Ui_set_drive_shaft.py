# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/simulate/set_drive_shaft.ui'
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
        self.label.setGeometry(QtCore.QRect(150, 150, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(150, 220, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 251, 51))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.Shaft_Center = QtWidgets.QComboBox(Dialog)
        self.Shaft_Center.setGeometry(QtCore.QRect(150, 180, 101, 25))
        self.Shaft_Center.setObjectName("Shaft_Center")
        self.References = QtWidgets.QComboBox(Dialog)
        self.References.setGeometry(QtCore.QRect(150, 250, 101, 25))
        self.References.setObjectName("References")
        self.Start_Angle = QtWidgets.QDoubleSpinBox(Dialog)
        self.Start_Angle.setGeometry(QtCore.QRect(30, 180, 91, 26))
        self.Start_Angle.setMinimum(0.0)
        self.Start_Angle.setMaximum(360.0)
        self.Start_Angle.setProperty("value", 0.0)
        self.Start_Angle.setObjectName("Start_Angle")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 81, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 80, 131, 21))
        self.label_5.setObjectName("label_5")
        self.Shaft_num = QtWidgets.QTextBrowser(Dialog)
        self.Shaft_num.setGeometry(QtCore.QRect(30, 110, 211, 31))
        self.Shaft_num.setObjectName("Shaft_num")
        self.End_Angle = QtWidgets.QDoubleSpinBox(Dialog)
        self.End_Angle.setGeometry(QtCore.QRect(30, 250, 91, 26))
        self.End_Angle.setMinimum(0.0)
        self.End_Angle.setMaximum(360.0)
        self.End_Angle.setProperty("value", 360.0)
        self.End_Angle.setObjectName("End_Angle")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 220, 81, 21))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Drive Shaft"))
        self.label.setText(_translate("Dialog", "Shaft Center"))
        self.label_2.setText(_translate("Dialog", "References"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Setting two Points for the New Drive Shaft.</span></p></body></html>"))
        self.Shaft_Center.setWhatsThis(_translate("Dialog", "Start point for next link."))
        self.References.setWhatsThis(_translate("Dialog", "End point for next link."))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>Start Angle</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>New Shaft number</p></body></html>"))
        self.label_6.setText(_translate("Dialog", "<html><head/><body><p>End Angle</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

