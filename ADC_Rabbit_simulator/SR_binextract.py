# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\doron\Documents\ADC_Rabbit_simulator\SR_binextract.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.open_flag = False
        self.Org_height = 750
        self.Org_width = 600
        self.object_list =[]
        MainWindow.resize(self.Org_width,  self.Org_height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Choose_SR = QtWidgets.QPushButton(self.centralwidget)
        self.Choose_SR.setGeometry(QtCore.QRect(10, 20, 141, 23))
        self.Choose_SR.setObjectName("Choose_SR")
        self.object_list.append(self.Choose_SR)
        self.label_SR = QtWidgets.QLabel(self.centralwidget)
        self.label_SR.setGeometry(QtCore.QRect(160, 20, 371, 21))
        self.label_SR.setObjectName("label_SR")
        self.object_list.append(self.label_SR)
        self.label_Ticket = QtWidgets.QLabel(self.centralwidget)
        self.label_Ticket.setGeometry(QtCore.QRect(160, 60, 371, 16))
        self.label_Ticket.setObjectName("label_Ticket")
        self.object_list.append(self.label_Ticket)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 110, 381, 521))
        self.listWidget.setObjectName("listWidget")
        self.object_list.append(self.listWidget)
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setGeometry(QtCore.QRect(20, 60, 131, 21))
        self.Start.setObjectName("Start")
        self.object_list.append(self.Start)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 590, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Choose_SR.setText(_translate("MainWindow", "Choose SR folder"))
        self.label_SR.setText(_translate("MainWindow", " Folder path:"))
        self.label_Ticket.setText(_translate("MainWindow", "Destination Path: C\\:temp"))
        self.Start.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
