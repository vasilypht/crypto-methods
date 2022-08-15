# Form implementation generated from reading ui file 'freqanalysis.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_freqanalysis(object):
    def setupUi(self, freqanalysis):
        freqanalysis.setObjectName("freqanalysis")
        freqanalysis.resize(1104, 696)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(freqanalysis)
        self.verticalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tab_widget = QtWidgets.QTabWidget(freqanalysis)
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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group_box_input)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_edit_input = QtWidgets.QTextEdit(self.group_box_input)
        self.text_edit_input.setObjectName("text_edit_input")
        self.verticalLayout_2.addWidget(self.text_edit_input)
        self.horizontalLayout.addWidget(self.group_box_input)
        self.group_box_output = QtWidgets.QGroupBox(self.tab_text)
        self.group_box_output.setObjectName("group_box_output")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.group_box_output)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_edit_output = QtWidgets.QTextEdit(self.group_box_output)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setObjectName("text_edit_output")
        self.verticalLayout.addWidget(self.text_edit_output)
        self.horizontalLayout.addWidget(self.group_box_output)
        self.tab_widget.addTab(self.tab_text, "")
        self.tab_document = QtWidgets.QWidget()
        self.tab_document.setObjectName("tab_document")
        self.tab_widget.addTab(self.tab_document, "")
        self.verticalLayout_5.addWidget(self.tab_widget)
        self.frame_1 = QtWidgets.QFrame(freqanalysis)
        self.frame_1.setMaximumSize(QtCore.QSize(16777215, 89))
        self.frame_1.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_1.setObjectName("frame_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_options = QtWidgets.QFrame(self.frame_1)
        self.frame_options.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_options.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_options.setObjectName("frame_options")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_options)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.group_box_options = QtWidgets.QGroupBox(self.frame_options)
        self.group_box_options.setObjectName("group_box_options")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.group_box_options)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(10)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.form_layout_options = QtWidgets.QFormLayout()
        self.form_layout_options.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.form_layout_options.setContentsMargins(4, -1, 4, -1)
        self.form_layout_options.setSpacing(10)
        self.form_layout_options.setObjectName("form_layout_options")
        self.label_lang = QtWidgets.QLabel(self.group_box_options)
        self.label_lang.setObjectName("label_lang")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_lang)
        self.combo_box_lang = QtWidgets.QComboBox(self.group_box_options)
        self.combo_box_lang.setObjectName("combo_box_lang")
        self.combo_box_lang.addItem("")
        self.combo_box_lang.addItem("")
        self.form_layout_options.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.combo_box_lang)
        self.combo_box_text_style = QtWidgets.QComboBox(self.group_box_options)
        self.combo_box_text_style.setObjectName("combo_box_text_style")
        self.combo_box_text_style.addItem("")
        self.combo_box_text_style.addItem("")
        self.combo_box_text_style.addItem("")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.combo_box_text_style)
        self.label_text_style = QtWidgets.QLabel(self.group_box_options)
        self.label_text_style.setObjectName("label_text_style")
        self.form_layout_options.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_text_style)
        self.verticalLayout_8.addLayout(self.form_layout_options)
        self.verticalLayout_4.addWidget(self.group_box_options)
        self.horizontalLayout_2.addWidget(self.frame_options)
        spacerItem = QtWidgets.QSpacerItem(132, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setSpacing(10)
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_1.setSpacing(10)
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")
        self.button_analysis = QtWidgets.QPushButton(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_analysis.sizePolicy().hasHeightForWidth())
        self.button_analysis.setSizePolicy(sizePolicy)
        self.button_analysis.setMinimumSize(QtCore.QSize(100, 30))
        self.button_analysis.setObjectName("button_analysis")
        self.horizontal_layout_1.addWidget(self.button_analysis)
        self.button_dechipher = QtWidgets.QPushButton(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_dechipher.sizePolicy().hasHeightForWidth())
        self.button_dechipher.setSizePolicy(sizePolicy)
        self.button_dechipher.setMinimumSize(QtCore.QSize(100, 30))
        self.button_dechipher.setObjectName("button_dechipher")
        self.horizontal_layout_1.addWidget(self.button_dechipher)
        self.vertical_layout_1.addLayout(self.horizontal_layout_1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout_1.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.vertical_layout_1)
        self.verticalLayout_5.addWidget(self.frame_1)
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setSpacing(10)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.group_box_graph = QtWidgets.QGroupBox(freqanalysis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_box_graph.sizePolicy().hasHeightForWidth())
        self.group_box_graph.setSizePolicy(sizePolicy)
        self.group_box_graph.setObjectName("group_box_graph")
        self.horizontal_layout_2.addWidget(self.group_box_graph)
        self.group_box_match_table = QtWidgets.QGroupBox(freqanalysis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_box_match_table.sizePolicy().hasHeightForWidth())
        self.group_box_match_table.setSizePolicy(sizePolicy)
        self.group_box_match_table.setMaximumSize(QtCore.QSize(200, 16777215))
        self.group_box_match_table.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.group_box_match_table.setObjectName("group_box_match_table")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_box_match_table)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.match_table_widget = QtWidgets.QTableWidget(self.group_box_match_table)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.match_table_widget.sizePolicy().hasHeightForWidth())
        self.match_table_widget.setSizePolicy(sizePolicy)
        self.match_table_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.match_table_widget.setObjectName("match_table_widget")
        self.match_table_widget.setColumnCount(0)
        self.match_table_widget.setRowCount(0)
        self.match_table_widget.horizontalHeader().setMinimumSectionSize(20)
        self.match_table_widget.verticalHeader().setDefaultSectionSize(30)
        self.match_table_widget.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout_3.addWidget(self.match_table_widget)
        self.horizontal_layout_2.addWidget(self.group_box_match_table)
        self.verticalLayout_5.addLayout(self.horizontal_layout_2)

        self.retranslateUi(freqanalysis)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(freqanalysis)

    def retranslateUi(self, freqanalysis):
        _translate = QtCore.QCoreApplication.translate
        freqanalysis.setWindowTitle(_translate("freqanalysis", "Form"))
        self.group_box_input.setTitle(_translate("freqanalysis", "Input text"))
        self.group_box_output.setTitle(_translate("freqanalysis", "Output text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_text), _translate("freqanalysis", "Text"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_document), _translate("freqanalysis", "Document"))
        self.group_box_options.setTitle(_translate("freqanalysis", "Options"))
        self.label_lang.setText(_translate("freqanalysis", "Language"))
        self.combo_box_lang.setItemText(0, _translate("freqanalysis", "English"))
        self.combo_box_lang.setItemText(1, _translate("freqanalysis", "Russian"))
        self.combo_box_text_style.setItemText(0, _translate("freqanalysis", "Common"))
        self.combo_box_text_style.setItemText(1, _translate("freqanalysis", "Literature"))
        self.combo_box_text_style.setItemText(2, _translate("freqanalysis", "Math"))
        self.label_text_style.setText(_translate("freqanalysis", "Text style"))
        self.button_analysis.setText(_translate("freqanalysis", "Analysis"))
        self.button_dechipher.setText(_translate("freqanalysis", "Dechipher"))
        self.group_box_graph.setTitle(_translate("freqanalysis", "Bar graph"))
        self.group_box_match_table.setTitle(_translate("freqanalysis", "Table ➤ Text"))
