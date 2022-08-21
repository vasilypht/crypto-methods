# Form implementation generated from reading ui file 'vigenere.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Vigenere(object):
    def setupUi(self, Vigenere):
        Vigenere.setObjectName("Vigenere")
        Vigenere.resize(733, 507)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Vigenere)
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tab_widget = QtWidgets.QTabWidget(Vigenere)
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
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.group_box_input)
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.text_edit_input = QtWidgets.QTextEdit(self.group_box_input)
        self.text_edit_input.setObjectName("text_edit_input")
        self.verticalLayout_28.addWidget(self.text_edit_input)
        self.horizontalLayout.addWidget(self.group_box_input)
        self.group_box_output = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_output.setObjectName("group_box_output")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.group_box_output)
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.text_edit_output = QtWidgets.QTextEdit(self.group_box_output)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setObjectName("text_edit_output")
        self.verticalLayout_29.addWidget(self.text_edit_output)
        self.horizontalLayout.addWidget(self.group_box_output)
        self.tab_widget.addTab(self.tab_text, "")
        self.verticalLayout_4.addWidget(self.tab_widget)
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.group_box_options = QtWidgets.QGroupBox(Vigenere)
        self.group_box_options.setMaximumSize(QtCore.QSize(400, 16777215))
        self.group_box_options.setObjectName("group_box_options")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group_box_options)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.form_layout_options = QtWidgets.QFormLayout()
        self.form_layout_options.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.form_layout_options.setContentsMargins(4, -1, 4, -1)
        self.form_layout_options.setObjectName("form_layout_options")
        self.label_key = QtWidgets.QLabel(self.group_box_options)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_key.sizePolicy().hasHeightForWidth())
        self.label_key.setSizePolicy(sizePolicy)
        self.label_key.setObjectName("label_key")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_key)
        self.line_edit_key = QtWidgets.QLineEdit(self.group_box_options)
        self.line_edit_key.setObjectName("line_edit_key")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_key)
        self.verticalLayout_2.addLayout(self.form_layout_options)
        self.vertical_layout_2.addWidget(self.group_box_options)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_2.addItem(spacerItem)
        self.horizontal_layout_1.addLayout(self.vertical_layout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_1.addItem(spacerItem1)
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.combo_box_enc_proc = QtWidgets.QComboBox(Vigenere)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_enc_proc.sizePolicy().hasHeightForWidth())
        self.combo_box_enc_proc.setSizePolicy(sizePolicy)
        self.combo_box_enc_proc.setObjectName("combo_box_enc_proc")
        self.horizontal_layout_2.addWidget(self.combo_box_enc_proc)
        self.button_make = QtWidgets.QPushButton(Vigenere)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_make.sizePolicy().hasHeightForWidth())
        self.button_make.setSizePolicy(sizePolicy)
        self.button_make.setMinimumSize(QtCore.QSize(100, 30))
        self.button_make.setObjectName("button_make")
        self.horizontal_layout_2.addWidget(self.button_make)
        self.vertical_layout_1.addLayout(self.horizontal_layout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_1.addItem(spacerItem2)
        self.horizontal_layout_1.addLayout(self.vertical_layout_1)
        self.verticalLayout_4.addLayout(self.horizontal_layout_1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 111, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)

        self.retranslateUi(Vigenere)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Vigenere)

    def retranslateUi(self, Vigenere):
        _translate = QtCore.QCoreApplication.translate
        Vigenere.setWindowTitle(_translate("Vigenere", "Form"))
        self.group_box_input.setTitle(_translate("Vigenere", "Input text"))
        self.group_box_output.setTitle(_translate("Vigenere", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("Vigenere", "Text"))
        self.group_box_options.setTitle(_translate("Vigenere", "Options"))
        self.label_key.setText(_translate("Vigenere", "Key:"))
        self.button_make.setText(_translate("Vigenere", "Make"))
