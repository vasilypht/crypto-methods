# Form implementation generated from reading ui file 'vernam.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_vernam(object):
    def setupUi(self, vernam):
        vernam.setObjectName("vernam")
        vernam.resize(622, 398)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(vernam)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tab_widget = QtWidgets.QTabWidget(vernam)
        self.tab_widget.setMaximumSize(QtCore.QSize(16777215, 400))
        self.tab_widget.setObjectName("tab_widget")
        self.tab_text = QtWidgets.QWidget()
        self.tab_text.setObjectName("tab_text")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_text)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.group_box_input = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_input.setObjectName("group_box_input")
        self.verticalLayout_42 = QtWidgets.QVBoxLayout(self.group_box_input)
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.text_edit_input = QtWidgets.QTextEdit(self.group_box_input)
        self.text_edit_input.setObjectName("text_edit_input")
        self.verticalLayout_42.addWidget(self.text_edit_input)
        self.horizontalLayout.addWidget(self.group_box_input)
        self.group_box_output = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_output.setObjectName("group_box_output")
        self.verticalLayout_43 = QtWidgets.QVBoxLayout(self.group_box_output)
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.text_edit_output = QtWidgets.QTextEdit(self.group_box_output)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setObjectName("text_edit_output")
        self.verticalLayout_43.addWidget(self.text_edit_output)
        self.horizontalLayout.addWidget(self.group_box_output)
        self.tab_widget.addTab(self.tab_text, "")
        self.verticalLayout_3.addWidget(self.tab_widget)
        self.horizontal_layout_3 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_3.setObjectName("horizontal_layout_3")
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.group_box_options = QtWidgets.QGroupBox(vernam)
        self.group_box_options.setMaximumSize(QtCore.QSize(400, 16777215))
        self.group_box_options.setObjectName("group_box_options")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.group_box_options)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.form_layout_options = QtWidgets.QFormLayout()
        self.form_layout_options.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.form_layout_options.setContentsMargins(4, -1, 4, -1)
        self.form_layout_options.setObjectName("form_layout_options")
        self.label_key = QtWidgets.QLabel(self.group_box_options)
        self.label_key.setObjectName("label_key")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_key)
        self.line_edit_key = QtWidgets.QLineEdit(self.group_box_options)
        self.line_edit_key.setText("")
        self.line_edit_key.setObjectName("line_edit_key")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_key)
        self.verticalLayout_4.addLayout(self.form_layout_options)
        self.vertical_layout_1.addWidget(self.group_box_options)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_1.addItem(spacerItem)
        self.horizontal_layout_3.addLayout(self.vertical_layout_1)
        spacerItem1 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_3.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.combo_box_enc_proc = QtWidgets.QComboBox(vernam)
        self.combo_box_enc_proc.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_box_enc_proc.setObjectName("combo_box_enc_proc")
        self.horizontal_layout_2.addWidget(self.combo_box_enc_proc)
        self.button_make = QtWidgets.QPushButton(vernam)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_make.sizePolicy().hasHeightForWidth())
        self.button_make.setSizePolicy(sizePolicy)
        self.button_make.setMinimumSize(QtCore.QSize(100, 30))
        self.button_make.setObjectName("button_make")
        self.horizontal_layout_2.addWidget(self.button_make)
        self.button_options = QtWidgets.QPushButton(vernam)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_options.sizePolicy().hasHeightForWidth())
        self.button_options.setSizePolicy(sizePolicy)
        self.button_options.setMinimumSize(QtCore.QSize(0, 30))
        self.button_options.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.button_options.setStyleSheet("")
        self.button_options.setText("")
        self.button_options.setIconSize(QtCore.QSize(16, 16))
        self.button_options.setDefault(False)
        self.button_options.setFlat(False)
        self.button_options.setObjectName("button_options")
        self.horizontal_layout_2.addWidget(self.button_options)
        self.verticalLayout.addLayout(self.horizontal_layout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontal_layout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontal_layout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 105, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)

        self.retranslateUi(vernam)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(vernam)

    def retranslateUi(self, vernam):
        _translate = QtCore.QCoreApplication.translate
        vernam.setWindowTitle(_translate("vernam", "Form"))
        self.group_box_input.setTitle(_translate("vernam", "Input text"))
        self.group_box_output.setTitle(_translate("vernam", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("vernam", "Text"))
        self.group_box_options.setTitle(_translate("vernam", "Options"))
        self.label_key.setText(_translate("vernam", "Key:"))
        self.button_make.setText(_translate("vernam", "Make"))
