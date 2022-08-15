# Form implementation generated from reading ui file 'xor.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_XOR(object):
    def setupUi(self, XOR):
        XOR.setObjectName("XOR")
        XOR.resize(549, 401)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(XOR)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tab_widget = QtWidgets.QTabWidget(XOR)
        self.tab_widget.setMaximumSize(QtCore.QSize(16777215, 400))
        self.tab_widget.setObjectName("tab_widget")
        self.tab_text = QtWidgets.QWidget()
        self.tab_text.setObjectName("tab_text")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_text)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.group_box_input = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_input.setObjectName("group_box_input")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_box_input)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.text_edit_input = QtWidgets.QTextEdit(self.group_box_input)
        self.text_edit_input.setObjectName("text_edit_input")
        self.verticalLayout_3.addWidget(self.text_edit_input)
        self.horizontalLayout_3.addWidget(self.group_box_input)
        self.group_box_output = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_output.setObjectName("group_box_output")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.group_box_output)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.text_edit_output = QtWidgets.QTextEdit(self.group_box_output)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setObjectName("text_edit_output")
        self.verticalLayout_4.addWidget(self.text_edit_output)
        self.horizontalLayout_3.addWidget(self.group_box_output)
        self.tab_widget.addTab(self.tab_text, "")
        self.tab_document = QtWidgets.QWidget()
        self.tab_document.setObjectName("tab_document")
        self.tab_widget.addTab(self.tab_document, "")
        self.verticalLayout_2.addWidget(self.tab_widget)
        self.frame_1 = QtWidgets.QFrame(XOR)
        self.frame_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_1.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_1.setObjectName("frame_1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.group_box_options = QtWidgets.QGroupBox(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_box_options.sizePolicy().hasHeightForWidth())
        self.group_box_options.setSizePolicy(sizePolicy)
        self.group_box_options.setMaximumSize(QtCore.QSize(400, 16777215))
        self.group_box_options.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.group_box_options.setFlat(False)
        self.group_box_options.setCheckable(False)
        self.group_box_options.setChecked(False)
        self.group_box_options.setObjectName("group_box_options")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.group_box_options)
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.form_layout_options = QtWidgets.QFormLayout()
        self.form_layout_options.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.form_layout_options.setContentsMargins(4, -1, 4, -1)
        self.form_layout_options.setObjectName("form_layout_options")
        self.line_edit_iv = QtWidgets.QLineEdit(self.group_box_options)
        self.line_edit_iv.setObjectName("line_edit_iv")
        self.form_layout_options.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_iv)
        self.label_gamma_size = QtWidgets.QLabel(self.group_box_options)
        self.label_gamma_size.setObjectName("label_gamma_size")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_gamma_size)
        self.spin_box_gamma_size = QtWidgets.QSpinBox(self.group_box_options)
        self.spin_box_gamma_size.setMinimumSize(QtCore.QSize(0, 0))
        self.spin_box_gamma_size.setMinimum(1)
        self.spin_box_gamma_size.setMaximum(100)
        self.spin_box_gamma_size.setProperty("value", 10)
        self.spin_box_gamma_size.setObjectName("spin_box_gamma_size")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_gamma_size)
        self.label_iv = QtWidgets.QLabel(self.group_box_options)
        self.label_iv.setObjectName("label_iv")
        self.form_layout_options.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_iv)
        self.label_iv_size = QtWidgets.QLabel(self.group_box_options)
        self.label_iv_size.setObjectName("label_iv_size")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_iv_size)
        self.spin_box_iv_size = QtWidgets.QSpinBox(self.group_box_options)
        self.spin_box_iv_size.setMinimum(1)
        self.spin_box_iv_size.setMaximum(100)
        self.spin_box_iv_size.setProperty("value", 10)
        self.spin_box_iv_size.setObjectName("spin_box_iv_size")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_iv_size)
        self.verticalLayout_6.addLayout(self.form_layout_options)
        self.vertical_layout_1.addWidget(self.group_box_options)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_1.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.vertical_layout_1)
        spacerItem1 = QtWidgets.QSpacerItem(138, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.combo_box_mode = QtWidgets.QComboBox(self.frame_1)
        self.combo_box_mode.setObjectName("combo_box_mode")
        self.combo_box_mode.addItem("")
        self.combo_box_mode.addItem("")
        self.horizontal_layout_2.addWidget(self.combo_box_mode)
        self.button_make = QtWidgets.QPushButton(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_make.sizePolicy().hasHeightForWidth())
        self.button_make.setSizePolicy(sizePolicy)
        self.button_make.setMinimumSize(QtCore.QSize(100, 30))
        self.button_make.setObjectName("button_make")
        self.horizontal_layout_2.addWidget(self.button_make)
        self.button_options = QtWidgets.QPushButton(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_options.sizePolicy().hasHeightForWidth())
        self.button_options.setSizePolicy(sizePolicy)
        self.button_options.setMinimumSize(QtCore.QSize(0, 30))
        self.button_options.setText("")
        self.button_options.setObjectName("button_options")
        self.horizontal_layout_2.addWidget(self.button_options)
        self.vertical_layout_2.addLayout(self.horizontal_layout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.vertical_layout_2)
        self.verticalLayout_2.addWidget(self.frame_1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)

        self.retranslateUi(XOR)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(XOR)

    def retranslateUi(self, XOR):
        _translate = QtCore.QCoreApplication.translate
        XOR.setWindowTitle(_translate("XOR", "Form"))
        self.group_box_input.setTitle(_translate("XOR", "Input text"))
        self.group_box_output.setTitle(_translate("XOR", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("XOR", "Text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_document), _translate("XOR", "Document"))
        self.group_box_options.setTitle(_translate("XOR", "Options"))
        self.label_gamma_size.setText(_translate("XOR", "Gamma size (bytes)"))
        self.label_iv.setText(_translate("XOR", "IV PRNG"))
        self.label_iv_size.setText(_translate("XOR", "IV size (bytes)"))
        self.combo_box_mode.setItemText(0, _translate("XOR", "Encrypt"))
        self.combo_box_mode.setItemText(1, _translate("XOR", "Decrypt"))
        self.button_make.setText(_translate("XOR", "Make"))
