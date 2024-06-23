from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem ,QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy
import pandas as pd
import pyarrow.parquet as pq
import shutil
import os
import polars as pl
from tkinter import messagebox, filedialog, Tk
from PIL import Image, ImageDraw
from VL_GUI import Ui_MainWindow
#from create_labels import my_function


class UI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_button_actions()

#------------- initialize all clickes --------------------------------------------------------------------------------------------------------------
    def init_button_actions(self):
        self.Select_folder.clicked.connect(self.clicked)
        self.Create_annon.clicked.connect(self.clicked)
        self.spinBox.valueChanged.connect(self.RoI_update)
        self.Create_annon.clicked.connect(self.Create_annonations)
        self.Root_path=""

    def clicked(self):
        sender = self.sender().objectName()
        if sender == "Select_folder":
            root = Tk()
            root.withdraw()
            self.Root_path = filedialog.askdirectory(title="select folder")
            self.Root_txt.setText("Root folder: " + self.Root_path)
            self.Update_image()
        else:
            if self.Root_path=="":
                QMessageBox.about(self, "info massage", "Please choose root folder first")
            else:

                self.Create_annonations()
                Case_study_n = self.Root_path.split("/")[-1]
                l= len(Case_study_n)
                #sys.argv.insert(1,self.Root_path)
                #sys.argv.insert(2,int(self.spinBox.value()))
                #sys.argv.insert(3,"test2")
                #x = my_function()
                archived = shutil.make_archive(self.Root_path[0:-l] + Case_study_n , 'zip', self.Root_path)
                if os.path.exists(self.Root_path[0:-l] + Case_study_n + '.zip'):
                    print(archived)
                else:
                    print("ZIP file not created")

    def get_Image(self,root_path):
        for root, dirs, files in os.walk(root_path):
            for file in files:
                arr = file.split(".")
                if os.path.normpath(arr[-1].lower()) in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']:
                    img_path = os.path.normpath(root + "/" + file)
                    return img_path

    def Update_image(self):
        self.curr_im = self.get_Image(self.Root_path)
        Img_pix = self.draw_ROI()
        self.label.setPixmap(Img_pix)

    def draw_ROI(self):
        ROI = self.spinBox.value()

        if not (self.curr_im is None):
            geo = self.label.geometry().getRect()
            Curr_im = Image.open(self.curr_im)
            self.Factor = Curr_im.size
            ROI_Resize = ROI*(max(geo)/max(self.Factor))
            resized_im = Curr_im.resize([geo[2], geo[3]])

            draw = ImageDraw.Draw(resized_im)
            middle_frame = geo[2] / 2
            draw.rectangle([middle_frame - ROI_Resize / 2,
                            middle_frame - ROI_Resize / 2,
                            middle_frame + ROI_Resize / 2,
                            middle_frame + ROI_Resize / 2],
                           outline="white", width=2)
            resized_im.save(os.getcwd() + '\\tmp.jpeg')
            pixmap = QPixmap(os.getcwd() + '\\tmp.jpeg')
            return(pixmap)

    def RoI_update(self):
        p=self.draw_ROI()
        self.label.setPixmap(p)

    def Create_annonations(self):
        bbox_map = {}
        default_width = int(self.spinBox.value())
        default_height = int(self.spinBox.value())

        data = []

        for dirpath, dirnames, filenames in os.walk(self.Root_path):
            for file in filenames:
                filepath = os.path.join(dirpath, file)
                filepath = filepath.replace("\\","/")

                try:
                    image = Image.open(filepath)

                    #filename = filename.replace("\\",'/')
                    tmp_str=filepath.split("/")
                    filename = tmp_str[-2] + "/" + file
                    label = tmp_str[-2]
                    bbox_width, bbox_height = bbox_map.get(label, (default_width, default_height))

                    center_x, center_y = image.width // 2, image.height // 2
                    bbox_x = center_x - bbox_width // 2
                    bbox_y = center_y - bbox_height // 2

                    data.append((filename, bbox_x, bbox_y, bbox_width, bbox_height, label))
                except Exception as e:
                    print(f'failed to load image: {filepath}: {e}')

        schema = {
            'filename': pl.Utf8,
            'col_x': pl.Int32,
            'row_y': pl.Int32,
            'width': pl.Int32,
            'height': pl.Int32,
            'label': pl.Utf8
        }
        annot = pl.DataFrame(data, schema=schema)
        annot.write_parquet(os.path.join(self.Root_path, 'object_annotations.parquet'))


if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    main_win=UI()
    main_win.show()
    app.exec_()
