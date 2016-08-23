# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/repeated_value.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_same_value(object):
    def setupUi(self, Warning_same_value):
        Warning_same_value.setObjectName("Warning_same_value")
        Warning_same_value.resize(411, 131)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_same_value.setWindowIcon(icon)
        Warning_same_value.setSizeGripEnabled(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_same_value)
        self.buttonBox.setGeometry(QtCore.QRect(320, 60, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Warning_same_value)
        self.label.setGeometry(QtCore.QRect(20, 20, 291, 91))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Warning_same_value)
        self.buttonBox.accepted.connect(Warning_same_value.accept)
        self.buttonBox.rejected.connect(Warning_same_value.reject)
        QtCore.QMetaObject.connectSlotsByName(Warning_same_value)

    def retranslateUi(self, Warning_same_value):
        _translate = QtCore.QCoreApplication.translate
        Warning_same_value.setWindowTitle(_translate("Warning_same_value", "Warning - Same Value"))
        self.label.setText(_translate("Warning_same_value", "<html><head/><body><p><span style=\" font-size:14pt;\">Can\'t use two same Essential elements.</span></p><p><span style=\" font-size:14pt;\">Please choose another requre entity.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_same_value = QtWidgets.QDialog()
    ui = Ui_Warning_same_value()
    ui.setupUi(Warning_same_value)
    Warning_same_value.show()
    sys.exit(app.exec_())

