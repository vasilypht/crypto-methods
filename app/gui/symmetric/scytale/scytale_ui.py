# Form implementation generated from reading ui file 'scytale.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Scytale(object):
    def setupUi(self, Scytale):
        Scytale.setObjectName("Scytale")
        Scytale.resize(905, 546)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Scytale)
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tab_widget = QtWidgets.QTabWidget(Scytale)
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
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.group_box_input)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.text_edit_input = QtWidgets.QTextEdit(self.group_box_input)
        self.text_edit_input.setObjectName("text_edit_input")
        self.verticalLayout_9.addWidget(self.text_edit_input)
        self.horizontalLayout.addWidget(self.group_box_input)
        self.group_box_output = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_output.setObjectName("group_box_output")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.group_box_output)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.text_edit_output = QtWidgets.QTextEdit(self.group_box_output)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setObjectName("text_edit_output")
        self.verticalLayout_8.addWidget(self.text_edit_output)
        self.horizontalLayout.addWidget(self.group_box_output)
        self.tab_widget.addTab(self.tab_text, "")
        self.verticalLayout_4.addWidget(self.tab_widget)
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.group_box_options = QtWidgets.QGroupBox(Scytale)
        self.group_box_options.setObjectName("group_box_options")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.group_box_options)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.form_layout_options = QtWidgets.QFormLayout()
        self.form_layout_options.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.form_layout_options.setContentsMargins(4, -1, 4, -1)
        self.form_layout_options.setObjectName("form_layout_options")
        self.label_rows = QtWidgets.QLabel(self.group_box_options)
        self.label_rows.setObjectName("label_rows")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_rows)
        self.spin_box_rows = QtWidgets.QSpinBox(self.group_box_options)
        self.spin_box_rows.setFrame(True)
        self.spin_box_rows.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spin_box_rows.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_box_rows.setMinimum(1)
        self.spin_box_rows.setMaximum(999)
        self.spin_box_rows.setProperty("value", 3)
        self.spin_box_rows.setObjectName("spin_box_rows")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_rows)
        self.check_box_columns = QtWidgets.QCheckBox(self.group_box_options)
        self.check_box_columns.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_box_columns.sizePolicy().hasHeightForWidth())
        self.check_box_columns.setSizePolicy(sizePolicy)
        self.check_box_columns.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.check_box_columns.setStyleSheet("color: grey")
        self.check_box_columns.setAutoExclusive(False)
        self.check_box_columns.setTristate(False)
        self.check_box_columns.setObjectName("check_box_columns")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.check_box_columns)
        self.spin_box_columns = QtWidgets.QSpinBox(self.group_box_options)
        self.spin_box_columns.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_box_columns.sizePolicy().hasHeightForWidth())
        self.spin_box_columns.setSizePolicy(sizePolicy)
        self.spin_box_columns.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spin_box_columns.setReadOnly(False)
        self.spin_box_columns.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_box_columns.setAccelerated(False)
        self.spin_box_columns.setMinimum(1)
        self.spin_box_columns.setMaximum(999)
        self.spin_box_columns.setProperty("value", 5)
        self.spin_box_columns.setObjectName("spin_box_columns")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_columns)
        self.verticalLayout.addLayout(self.form_layout_options)
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
        self.combo_box_mode = QtWidgets.QComboBox(Scytale)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_mode.sizePolicy().hasHeightForWidth())
        self.combo_box_mode.setSizePolicy(sizePolicy)
        self.combo_box_mode.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.combo_box_mode.setFrame(True)
        self.combo_box_mode.setObjectName("combo_box_mode")
        self.combo_box_mode.addItem("")
        self.combo_box_mode.addItem("")
        self.horizontal_layout_2.addWidget(self.combo_box_mode)
        self.button_make = QtWidgets.QPushButton(Scytale)
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
        spacerItem3 = QtWidgets.QSpacerItem(20, 128, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)

        self.retranslateUi(Scytale)
        QtCore.QMetaObject.connectSlotsByName(Scytale)

    def retranslateUi(self, Scytale):
        _translate = QtCore.QCoreApplication.translate
        Scytale.setWindowTitle(_translate("Scytale", "Form"))
        self.group_box_input.setTitle(_translate("Scytale", "Input text"))
        self.group_box_output.setTitle(_translate("Scytale", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("Scytale", "Text"))
        self.group_box_options.setTitle(_translate("Scytale", "Options"))
        self.label_rows.setText(_translate("Scytale", "Number of rows:"))
        self.check_box_columns.setText(_translate("Scytale", "Custom number of columns:"))
        self.combo_box_mode.setItemText(0, _translate("Scytale", "Encrypt"))
        self.combo_box_mode.setItemText(1, _translate("Scytale", "Decrypt"))
        self.button_make.setText(_translate("Scytale", "Make"))
