# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\doron\Documents\ADC utility tool\Image plot.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QMainWindow,QTableWidgetItem
import os
from PyQt5.QtGui import QPixmap
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw

class Ui_plot_image(object):
    def setupUi(self, plot_image):
        plot_image.setObjectName("plot_image")
        plot_image.resize(644, 662)
        self.centralwidget = QtWidgets.QWidget(plot_image)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 10, 501, 501))
        self.label.setText("")
        self.label.setObjectName("label")
        self.Button_prev = QtWidgets.QPushButton(self.centralwidget)
        self.Button_prev.setGeometry(QtCore.QRect(470, 550, 75, 23))
        self.Button_prev.setObjectName("Button_prev")
        self.Button_del = QtWidgets.QPushButton(self.centralwidget)
        self.Button_del.setGeometry(QtCore.QRect(10, 550, 75, 23))
        self.Button_del.setObjectName("Button_del")
        self.Button_next = QtWidgets.QPushButton(self.centralwidget)
        self.Button_next.setGeometry(QtCore.QRect(550, 550, 75, 23))
        self.Button_next.setObjectName("Button_next")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(6, 523, 621, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 550, 361, 21))
        self.label_3.setObjectName("label_3")
        self.Next_row_im = QtWidgets.QPushButton(self.centralwidget)
        self.Next_row_im.setGeometry(QtCore.QRect(310, 590, 111, 23))
        self.Next_row_im.setObjectName("Next_row_im")
        self.Prev_row_im = QtWidgets.QPushButton(self.centralwidget)
        self.Prev_row_im.setGeometry(QtCore.QRect(200, 590, 111, 23))
        self.Prev_row_im.setObjectName("Prev_row_im")
        plot_image.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(plot_image)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 644, 22))
        self.menubar.setObjectName("menubar")
        plot_image.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(plot_image)
        self.statusbar.setObjectName("statusbar")
        plot_image.setStatusBar(self.statusbar)

        self.retranslateUi(plot_image)
        QtCore.QMetaObject.connectSlotsByName(plot_image)

    def retranslateUi(self, plot_image):
        _translate = QtCore.QCoreApplication.translate
        plot_image.setWindowTitle(_translate("plot_image", "MainWindow"))
        self.Button_prev.setText(_translate("plot_image", "Prev image"))
        self.Button_del.setText(_translate("plot_image", "Delete Image"))
        self.Button_next.setText(_translate("plot_image", "Next Image"))
        self.label_2.setText(_translate("plot_image", "Image Path:"))
        self.label_3.setText(_translate("plot_image", "Class Lable:"))
        self.Next_row_im.setText(_translate("plot_image", "Next row image"))
        self.Prev_row_im.setText(_translate("plot_image", "Prev row image"))

class page(Ui_plot_image, QMainWindow):
    def __init__(self,table):
        super().__init__()
        self.setupUi(self)
        self.table = table
        self.start_init()

    def start_init(self):
        self.Button_next.clicked.connect(self.Page_event)
        self.Button_prev.clicked.connect(self.Page_event)
        self.Button_del.clicked.connect(self.Page_event)
        self.Next_row_im.clicked.connect(self.Page_event)
        self.Prev_row_im.clicked.connect(self.Page_event)
        self.hist = 0
        self.r = None
        self.c = None
        self.similar_analysis = 0

    def Page_event(self):
        column_max = self.table.columnCount()
        sender = self.Main_window.sender()
        if self.r == None and self.c == None:
            self.c = self.table.currentColumn()
            self.r = self.table.currentRow()
        if sender.objectName() == "Button_del":
            self.delete_image()
        elif sender.objectName() == "Button_next":
            self.next_image()
        elif sender.objectName() == "Button_prev":
            self.prev_image()
        elif sender.objectName() == "Prev_row_im":
            self.Prev_row_image()
        elif sender.objectName() == "Next_row_im":
            self.Next_row_image()

    def next_image(self):
        try:
            column_max = self.table.columnCount()
            if self.r == None and self.c == None:
                self.c = self.table.currentColumn()
                self.r = self.table.currentRow()
            if self.c + 1  == column_max :
               self.Button_prev.show()
               self.Button_next.hide()
            else:
                if self.c + 2 >= column_max:
                    self.Button_next.hide()
                else:
                    self.Button_next.show()
                self.c = self.c + 1
                self.Button_prev.show()
            if self.similar_analysis == 0:
                self.update_image(os.path.normpath(self.duplicates2[self.r][self.c]))
            else:
                self.update_image(os.path.normpath(self.duplicates2[self.r]))
        except:
            self.c = self.c - 1
            messagebox.showinfo(title='Error massage', message='empty cell')
        #self.show_hide_buttons(flag)

    def prev_image(self):
        r_c = self.table.columnCount()
        if self.r == None and self.c == None:
            self.c = self.table.currentColumn()
            self.r = self.table.currentRow()

        if self.c  == 0:
            self.Button_prev.hide()
            self.Button_next.show()
        else:
            if self.c - 1 == 0 :
                self.Button_prev.hide()
            else:
                self.Button_prev.show()
            self.c = self.c - 1
            self.Button_next.show()
        try:
            if self.similar_analysis == 0:
                self.update_image(os.path.normpath(self.duplicates2[self.r][self.c]))
            else:
                self.update_image(os.path.normpath(self.duplicates2[self.r]))
        except:
            messagebox.showinfo(title='Error massage', message='empty cell')

    def delete_image(self):
        try:
            os.remove(self.curr_file)
            table_len = self.table.columnCount()
            cnt=0
            self.table.setItem(self.r,self.c,QTableWidgetItem(''))
            #for i in range(table_len):
                #if self.table.item(self.r,i).text() != '':
                    #cnt += 1
            #if cnt < 2:
                #self.tableWidget.removeRow(self.r)


            self.Next_row_image()
        except:
            messagebox.showinfo(title='Error massage', message='Image is not exist')

    def update_image(self,path):
        ROI = self.ROI
        im = Image.open(path)
        geo = self.label.geometry().getRect()
        resized_im = im.resize([geo[2], geo[3]])
        draw = ImageDraw.Draw(resized_im)
        middle_frame = geo[2] / 2
        draw.rectangle([middle_frame - ROI / 2,
                        middle_frame - ROI / 2,
                        middle_frame + ROI / 2,
                        middle_frame + ROI / 2],
                       outline="blue", width=2)
        resized_im.save(os.getcwd() + '\\tmp.jpeg')
        pixmap = QPixmap(os.getcwd() + '\\tmp.jpeg')


        self.label_2.setText("Image path: " + path)
        self.curr_file = path
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        tmp = path.split("\\")
        self.label_3.setText("Class lable: " + tmp[-2])
        self.label_3.setStyleSheet("color : red")

    def draw_ROI(self):
        im = self.curr_im
        ROI = self.spinBox_ROI.value()
        geo = self.label_8.geometry().getRect()
        resized_im = im.resize([geo[2], geo[3]])
        draw = ImageDraw.Draw(resized_im)
        middle_frame = geo[2] / 2
        draw.rectangle([middle_frame - ROI / 2,
                        middle_frame - ROI / 2,
                        middle_frame + ROI / 2,
                        middle_frame + ROI / 2],
                       outline="blue", width=2)
        resized_im.save(os.getcwd() + '\\tmp.jpeg')
        pixmap = QPixmap(os.getcwd() + '\\tmp.jpeg')
        self.label_8.setPixmap(pixmap)

    def Next_row_image(self):
        r_c = self.table.rowCount()
        if self.r == None and self.c == None:
            self.c = self.table.currentColumn()
            self.r = self.table.currentRow()

        if self.r != r_c:
            self.r = self.r +1
            try:
                if not self.hist:
                    l = len(os.path.normpath(self.duplicates2[self.r][self.c]))
                    if l > 1:
                        self.update_image(os.path.normpath(self.duplicates2[self.r][self.c]))
                    else:
                        self.update_image(os.path.normpath(self.duplicates2[self.r]))
                else:
                    self.update_image(os.path.normpath(self.duplicates2[self.r]))
            except:
                messagebox.showinfo(title='Error massage', message='empty cell')
        else:
            messagebox.showinfo(title='Error massage', message='end of the image list')

    def Prev_row_image(self):
        r_c = self.table.rowCount()
        if self.r == None and self.c == None:
            self.c = self.table.currentColumn()
            self.r = self.table.currentRow()

        if self.r != 0:
            self.r = self.r - 1
            try:
                if not self.hist:
                    l = len(os.path.normpath(self.duplicates2[self.r][self.c]))
                    if l > 1:
                        self.update_image(os.path.normpath(self.duplicates2[self.r][self.c]))
                    else:
                        self.update_image(os.path.normpath(self.duplicates2[self.r]))
                else:
                    self.update_image(os.path.normpath(self.duplicates2[self.r]))
            except:
                messagebox.showinfo(title='Error massage', message='empty cell')
        else:
            messagebox.showinfo(title='Error massage', message='head of the image list')

    def show_hide_buttons(self):
        button = self.Main_window.sender().objectName()
        r_c = self.table.rowCount()
        if self.r == None and self.c == None:
            self.c = self.table.currentColumn()
            self.r = self.table.currentRow()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    plot_image = QtWidgets.QMainWindow()
    ui = Ui_plot_image()
    ui.setupUi(plot_image)
    plot_image.show()
    sys.exit(app.exec_())
