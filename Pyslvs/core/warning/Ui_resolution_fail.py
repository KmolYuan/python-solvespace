# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/resolution_fail.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_resolution_fail(object):
    def setupUi(self, Warning_resolution_fail):
        Warning_resolution_fail.setObjectName("Warning_resolution_fail")
        Warning_resolution_fail.resize(411, 160)
        Warning_resolution_fail.setMinimumSize(QtCore.QSize(411, 160))
        Warning_resolution_fail.setMaximumSize(QtCore.QSize(411, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/sketch-in-plane.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_resolution_fail.setWindowIcon(icon)
        Warning_resolution_fail.setSizeGripEnabled(True)
        Warning_resolution_fail.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_resolution_fail)
        self.buttonBox.setGeometry(QtCore.QRect(320, 90, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Warning_resolution_fail)
        self.label.setGeometry(QtCore.QRect(30, 20, 281, 131))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Warning_resolution_fail)
        self.buttonBox.accepted.connect(Warning_resolution_fail.accept)
        self.buttonBox.rejected.connect(Warning_resolution_fail.reject)
        QtCore.QMetaObject.connectSlotsByName(Warning_resolution_fail)

    def retranslateUi(self, Warning_resolution_fail):
        _translate = QtCore.QCoreApplication.translate
        Warning_resolution_fail.setWindowTitle(_translate("Warning_resolution_fail", "Warning - Resolution failed"))
        self.label.setText(_translate("Warning_resolution_fail", "<html><head/><body><p><span style=\" font-size:16pt;\">Resolution failed.</span></p><p><span style=\" font-size:12pt;\">Please checkout Command logs or tables see what happend with the Entities.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_resolution_fail = QtWidgets.QDialog()
    ui = Ui_Warning_resolution_fail()
    ui.setupUi(Warning_resolution_fail)
    Warning_resolution_fail.show()
    sys.exit(app.exec_())

