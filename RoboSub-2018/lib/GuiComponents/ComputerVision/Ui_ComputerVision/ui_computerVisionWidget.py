# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_computerVisionWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ComputerVisionWidget(object):
    def setupUi(self, ComputerVisionWidget):
        ComputerVisionWidget.setObjectName(_fromUtf8("ComputerVisionWidget"))
        ComputerVisionWidget.resize(807, 542)
        self.horizontalLayout = QtGui.QHBoxLayout(ComputerVisionWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Left_Camera = QtGui.QLabel(ComputerVisionWidget)
        self.Left_Camera.setEnabled(True)
        self.Left_Camera.setMinimumSize(QtCore.QSize(30, 30))
        self.Left_Camera.setScaledContents(True)
        self.Left_Camera.setObjectName(_fromUtf8("Left_Camera"))
        self.horizontalLayout_2.addWidget(self.Left_Camera)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.hideSettingsButton = QtGui.QPushButton(ComputerVisionWidget)
        self.hideSettingsButton.setObjectName(_fromUtf8("hideSettingsButton"))
        self.verticalLayout_2.addWidget(self.hideSettingsButton)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.settingsWidget = QtGui.QWidget(ComputerVisionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsWidget.sizePolicy().hasHeightForWidth())
        self.settingsWidget.setSizePolicy(sizePolicy)
        self.settingsWidget.setObjectName(_fromUtf8("settingsWidget"))
        self.gridLayout = QtGui.QGridLayout(self.settingsWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.settingsWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.selectCameraCB = QtGui.QComboBox(self.settingsWidget)
        self.selectCameraCB.setObjectName(_fromUtf8("selectCameraCB"))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.selectCameraCB.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.selectCameraCB)
        self.label_3 = QtGui.QLabel(self.settingsWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_2 = QtGui.QLabel(self.settingsWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.formLayout_2.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_9)
        self.label_4 = QtGui.QLabel(self.settingsWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.formLayout_2.setLayout(7, QtGui.QFormLayout.FieldRole, self.horizontalLayout_10)
        self.label_5 = QtGui.QLabel(self.settingsWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.formLayout_2.setLayout(8, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_6 = QtGui.QLabel(self.settingsWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_11.addLayout(self.verticalLayout_8)
        self.formLayout_2.setLayout(9, QtGui.QFormLayout.FieldRole, self.horizontalLayout_11)
        self.missionList = QtGui.QComboBox(self.settingsWidget)
        self.missionList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.missionList.setObjectName(_fromUtf8("missionList"))
        self.missionList.addItem(_fromUtf8(""))
        self.missionList.addItem(_fromUtf8(""))
        self.missionList.addItem(_fromUtf8(""))
        self.missionList.addItem(_fromUtf8(""))
        self.missionList.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(12, QtGui.QFormLayout.FieldRole, self.missionList)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.saveImageSettingsButton = QtGui.QPushButton(self.settingsWidget)
        self.saveImageSettingsButton.setObjectName(_fromUtf8("saveImageSettingsButton"))
        self.horizontalLayout_3.addWidget(self.saveImageSettingsButton)
        self.formLayout_2.setLayout(13, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.useImageButton = QtGui.QPushButton(self.settingsWidget)
        self.useImageButton.setObjectName(_fromUtf8("useImageButton"))
        self.horizontalLayout_12.addWidget(self.useImageButton)
        self.imagePathLineEdit = QtGui.QLineEdit(self.settingsWidget)
        self.imagePathLineEdit.setObjectName(_fromUtf8("imagePathLineEdit"))
        self.horizontalLayout_12.addWidget(self.imagePathLineEdit)
        self.runImageButton = QtGui.QPushButton(self.settingsWidget)
        self.runImageButton.setObjectName(_fromUtf8("runImageButton"))
        self.horizontalLayout_12.addWidget(self.runImageButton)
        self.formLayout_2.setLayout(14, QtGui.QFormLayout.FieldRole, self.horizontalLayout_12)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.useVideoButton = QtGui.QPushButton(self.settingsWidget)
        self.useVideoButton.setObjectName(_fromUtf8("useVideoButton"))
        self.horizontalLayout_14.addWidget(self.useVideoButton)
        self.videoPathLineEdit = QtGui.QLineEdit(self.settingsWidget)
        self.videoPathLineEdit.setObjectName(_fromUtf8("videoPathLineEdit"))
        self.horizontalLayout_14.addWidget(self.videoPathLineEdit)
        self.runVideoButton = QtGui.QPushButton(self.settingsWidget)
        self.runVideoButton.setObjectName(_fromUtf8("runVideoButton"))
        self.horizontalLayout_14.addWidget(self.runVideoButton)
        self.formLayout_2.setLayout(16, QtGui.QFormLayout.FieldRole, self.horizontalLayout_14)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_16)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.findModelButton = QtGui.QPushButton(self.settingsWidget)
        self.findModelButton.setObjectName(_fromUtf8("findModelButton"))
        self.horizontalLayout_17.addWidget(self.findModelButton)
        self.useNNCheckBox = QtGui.QCheckBox(self.settingsWidget)
        self.useNNCheckBox.setObjectName(_fromUtf8("useNNCheckBox"))
        self.horizontalLayout_17.addWidget(self.useNNCheckBox)
        self.modelPathLineEdit = QtGui.QLineEdit(self.settingsWidget)
        self.modelPathLineEdit.setObjectName(_fromUtf8("modelPathLineEdit"))
        self.horizontalLayout_17.addWidget(self.modelPathLineEdit)
        self.formLayout_2.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_17)
        self.hsiMaxLayout = QtGui.QHBoxLayout()
        self.hsiMaxLayout.setObjectName(_fromUtf8("hsiMaxLayout"))
        self.formLayout_2.setLayout(10, QtGui.QFormLayout.FieldRole, self.hsiMaxLayout)
        self.label_7 = QtGui.QLabel(self.settingsWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_7)
        self.hsiMinLayout = QtGui.QHBoxLayout()
        self.hsiMinLayout.setObjectName(_fromUtf8("hsiMinLayout"))
        self.formLayout_2.setLayout(11, QtGui.QFormLayout.FieldRole, self.hsiMinLayout)
        self.label_8 = QtGui.QLabel(self.settingsWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_8)
        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.settingsWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(ComputerVisionWidget)
        QtCore.QMetaObject.connectSlotsByName(ComputerVisionWidget)

    def retranslateUi(self, ComputerVisionWidget):
        ComputerVisionWidget.setWindowTitle(_translate("ComputerVisionWidget", "Form", None))
        self.Left_Camera.setText(_translate("ComputerVisionWidget", "Left_Camera", None))
        self.hideSettingsButton.setText(_translate("ComputerVisionWidget", "Hide Settings", None))
        self.label.setText(_translate("ComputerVisionWidget", "Camera:", None))
        self.selectCameraCB.setItemText(0, _translate("ComputerVisionWidget", "1", None))
        self.selectCameraCB.setItemText(1, _translate("ComputerVisionWidget", "2", None))
        self.selectCameraCB.setItemText(2, _translate("ComputerVisionWidget", "3", None))
        self.selectCameraCB.setItemText(3, _translate("ComputerVisionWidget", "4", None))
        self.selectCameraCB.setItemText(4, _translate("ComputerVisionWidget", "1 & 2 disparity", None))
        self.selectCameraCB.setItemText(5, _translate("ComputerVisionWidget", "3 & 4 disparity", None))
        self.label_3.setText(_translate("ComputerVisionWidget", "Neural Network Model:", None))
        self.label_2.setText(_translate("ComputerVisionWidget", "HSV Max", None))
        self.label_4.setText(_translate("ComputerVisionWidget", "HSV Min", None))
        self.label_5.setText(_translate("ComputerVisionWidget", "Canny Edge Params", None))
        self.label_6.setText(_translate("ComputerVisionWidget", "Stereo Vision Params", None))
        self.missionList.setItemText(0, _translate("ComputerVisionWidget", "Torpedo", None))
        self.missionList.setItemText(1, _translate("ComputerVisionWidget", "Dropper", None))
        self.missionList.setItemText(2, _translate("ComputerVisionWidget", "Red Buoy", None))
        self.missionList.setItemText(3, _translate("ComputerVisionWidget", "Green Buoy", None))
        self.missionList.setItemText(4, _translate("ComputerVisionWidget", "Yellow Anchor", None))
        self.saveImageSettingsButton.setText(_translate("ComputerVisionWidget", "Save Image Settings", None))
        self.useImageButton.setText(_translate("ComputerVisionWidget", "Browse Images", None))
        self.runImageButton.setText(_translate("ComputerVisionWidget", "Run Image", None))
        self.useVideoButton.setText(_translate("ComputerVisionWidget", "Browse Videos", None))
        self.runVideoButton.setText(_translate("ComputerVisionWidget", "Run Video", None))
        self.findModelButton.setText(_translate("ComputerVisionWidget", "Find Model", None))
        self.useNNCheckBox.setText(_translate("ComputerVisionWidget", "Use Neural Network", None))
        self.label_7.setText(_translate("ComputerVisionWidget", "HSI Max", None))
        self.label_8.setText(_translate("ComputerVisionWidget", "HSI Min", None))

