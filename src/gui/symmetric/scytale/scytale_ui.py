# Form implementation generated from reading ui file 'scytale.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_scytale(object):
    def setupUi(self, scytale):
        scytale.setObjectName("scytale")
        scytale.resize(651, 334)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(scytale)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tab_widget = QtWidgets.QTabWidget(scytale)
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
        self.verticalLayout_2.addWidget(self.tab_widget, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_1.addItem(spacerItem)
        self.form_layout_1 = QtWidgets.QFormLayout()
        self.form_layout_1.setObjectName("form_layout_1")
        self.label_rows = QtWidgets.QLabel(scytale)
        self.label_rows.setObjectName("label_rows")
        self.form_layout_1.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_rows)
        self.spin_box_rows = QtWidgets.QSpinBox(scytale)
        self.spin_box_rows.setFrame(True)
        self.spin_box_rows.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spin_box_rows.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_box_rows.setMinimum(1)
        self.spin_box_rows.setMaximum(999)
        self.spin_box_rows.setProperty("value", 3)
        self.spin_box_rows.setObjectName("spin_box_rows")
        self.form_layout_1.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_rows)
        self.check_box_columns = QtWidgets.QCheckBox(scytale)
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
        self.form_layout_1.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.check_box_columns)
        self.spin_box_columns = QtWidgets.QSpinBox(scytale)
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
        self.form_layout_1.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_columns)
        self.horizontal_layout_1.addLayout(self.form_layout_1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_1.addItem(spacerItem1)
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.combo_box_mode = QtWidgets.QComboBox(scytale)
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
        self.vertical_layout_1.addWidget(self.combo_box_mode)
        self.button_make = QtWidgets.QPushButton(scytale)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_make.sizePolicy().hasHeightForWidth())
        self.button_make.setSizePolicy(sizePolicy)
        self.button_make.setMinimumSize(QtCore.QSize(100, 30))
        self.button_make.setObjectName("button_make")
        self.vertical_layout_1.addWidget(self.button_make)
        self.horizontal_layout_1.addLayout(self.vertical_layout_1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_1.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontal_layout_1)
        spacerItem3 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)

        self.retranslateUi(scytale)
        QtCore.QMetaObject.connectSlotsByName(scytale)

    def retranslateUi(self, scytale):
        _translate = QtCore.QCoreApplication.translate
        scytale.setWindowTitle(_translate("scytale", "Form"))
        self.group_box_input.setTitle(_translate("scytale", "Input text"))
        self.group_box_output.setTitle(_translate("scytale", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("scytale", "Text"))
        self.label_rows.setText(_translate("scytale", "Number of rows:"))
        self.check_box_columns.setText(_translate("scytale", "Custom number of columns:"))
        self.combo_box_mode.setItemText(0, _translate("scytale", "Encrypt"))
        self.combo_box_mode.setItemText(1, _translate("scytale", "Decrypt"))
        self.button_make.setText(_translate("scytale", "Make"))
