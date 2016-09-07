# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/simulate/run_Measurement.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(399, 88)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 88))
        Form.setMouseTracking(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.Distance = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Distance.sizePolicy().hasHeightForWidth())
        self.Distance.setSizePolicy(sizePolicy)
        self.Distance.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Distance.setObjectName("Distance")
        self.horizontalLayout_3.addWidget(self.Distance)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.Mouse = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mouse.sizePolicy().hasHeightForWidth())
        self.Mouse.setSizePolicy(sizePolicy)
        self.Mouse.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Mouse.setObjectName("Mouse")
        self.horizontalLayout_3.addWidget(self.Mouse)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.start = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setMaximumSize(QtCore.QSize(16777215, 30))
        self.start.setObjectName("start")
        self.horizontalLayout_2.addWidget(self.start)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.end = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy)
        self.end.setMaximumSize(QtCore.QSize(16777215, 30))
        self.end.setObjectName("end")
        self.horizontalLayout_2.addWidget(self.end)
        self.CloseButton = QtWidgets.QPushButton(Form)
        self.CloseButton.setObjectName("CloseButton")
        self.horizontalLayout_2.addWidget(self.CloseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        self.CloseButton.clicked.connect(Form.deleteLater)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Distance:"))
        self.label.setText(_translate("Form", "Mouse position:"))
        self.label_3.setText(_translate("Form", "From:"))
        self.label_2.setText(_translate("Form", "To:"))
        self.CloseButton.setText(_translate("Form", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

