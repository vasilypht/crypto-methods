# Form implementation generated from reading ui file 'dragdrop_upload_widget.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DragDropUploadWidget(object):
    def setupUi(self, DragDropUploadWidget):
        DragDropUploadWidget.setObjectName("DragDropUploadWidget")
        DragDropUploadWidget.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        DragDropUploadWidget.resize(656, 374)
        self.verticalLayout = QtWidgets.QVBoxLayout(DragDropUploadWidget)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_dragdrop = QtWidgets.QPushButton(DragDropUploadWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_dragdrop.sizePolicy().hasHeightForWidth())
        self.button_dragdrop.setSizePolicy(sizePolicy)
        self.button_dragdrop.setObjectName("button_dragdrop")
        self.verticalLayout.addWidget(self.button_dragdrop)

        self.retranslateUi(DragDropUploadWidget)
        QtCore.QMetaObject.connectSlotsByName(DragDropUploadWidget)

    def retranslateUi(self, DragDropUploadWidget):
        _translate = QtCore.QCoreApplication.translate
        DragDropUploadWidget.setWindowTitle(_translate("DragDropUploadWidget", "Form"))
        self.button_dragdrop.setText(_translate("DragDropUploadWidget", "Choose a file or drag it here."))