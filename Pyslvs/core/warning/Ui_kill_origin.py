# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/kill_origin.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_kill_origin(object):
    def setupUi(self, Warning_kill_origin):
        Warning_kill_origin.setObjectName("Warning_kill_origin")
        Warning_kill_origin.resize(411, 160)
        Warning_kill_origin.setMinimumSize(QtCore.QSize(411, 160))
        Warning_kill_origin.setMaximumSize(QtCore.QSize(411, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_kill_origin.setWindowIcon(icon)
        Warning_kill_origin.setSizeGripEnabled(True)
        Warning_kill_origin.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_kill_origin)
        self.buttonBox.setGeometry(QtCore.QRect(320, 90, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Warning_kill_origin)
        self.label.setGeometry(QtCore.QRect(50, 10, 291, 131))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Warning_kill_origin)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 31, 31))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/delete.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Warning_kill_origin)
        self.buttonBox.accepted.connect(Warning_kill_origin.accept)
        self.buttonBox.rejected.connect(Warning_kill_origin.reject)
        QtCore.QMetaObject.connectSlotsByName(Warning_kill_origin)

    def retranslateUi(self, Warning_kill_origin):
        _translate = QtCore.QCoreApplication.translate
        Warning_kill_origin.setWindowTitle(_translate("Warning_kill_origin", "Warning - Kill Origin"))
        self.label.setText(_translate("Warning_kill_origin", "<html><head/><body><p><span style=\" font-size:20pt;\">I just stand HERE...</span></p><p><span style=\" font-size:10pt;\">Origin can\'t delete.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_kill_origin = QtWidgets.QDialog()
    ui = Ui_Warning_kill_origin()
    ui.setupUi(Warning_kill_origin)
    Warning_kill_origin.show()
    sys.exit(app.exec_())

