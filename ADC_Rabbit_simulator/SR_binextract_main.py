import os
import sys
import shutil
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from SR_binextract import Ui_MainWindow
import xmltodict
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class Copy_Worker(QThread):
    generating_ticket_done = pyqtSignal(str)  # Signal to indicate the comparison is done
    stop_requested = pyqtSignal(bool)

    def __init__(self,SR_path):
        super(Copy_Worker,self).__init__()
        self.SR_path = SR_path
        self.stop_requested = False

        dict = self.Read_XML_file(os.getcwd())
        self.destination = dict["root"]["Output_folder_name"]

    def stop(self):
        self.stop_requested = True
        #self.generating_ticket_done.emit("Worker have been stopped")

    def Read_XML_file(self,path):
        with open(os.path.normpath(path + '\\config.xml')) as fd:
            doc = xmltodict.parse(fd.read())
        return doc
        fd.close()

    def copy_image(self):
        x=1

    def run(self):
        for root, dirs, files in os.walk(self.SR_path):
            if self.stop_requested:
                break
            if "ScanLog.ini" in files:
                try:
                    cmd = 'ExportAdc.exe -srp ' '"' + root + '"' ' /cld:-1 /cd:-1 /tm:surface=0,chipping=1,prob=2'
                    subprocess.run(cmd, shell=True, check=True)
                    print("Executable ran successfully.")
                    if os.path.exists(root + "\\ADC\\Surface2Bump.csv"):
                        data_frame = pd.read_csv(root + "\\ADC\\Surface2Bump.csv")
                        df_size = data_frame.shape
                        df = pd.DataFrame(data_frame)
                        SR_path = root.replace('/', '\\')
                        tmp_str = SR_path.split("\\")
                        job = tmp_str[-4]
                        setup = tmp_str[-3]
                        lot = tmp_str[-2]
                        wafer = tmp_str[-1]
                        for i in range(df_size[0]):
                            if self.stop_requested:
                                break
                            try:
                                bin = str(df[' OClass'][i])
                                img_name = df['ImageName'][i]
                                if not os.path.exists(self.destination + "\\" + job + "\\" + bin):
                                    os.makedirs(self.destination  + "\\" + job + "\\" + bin)
                                shutil.copy(SR_path + "\\" + img_name,
                                            self.destination  + "\\" + job + "\\" + bin + "\\" + img_name)
                            except:
                                self.generating_ticket_done.emit(
                                    str("coudn't copy the image" + job + "\\" + bin + "\\" + img_name))
                    self.generating_ticket_done.emit(str("images was seperated for wafer ->" + job + "\\" + setup + "\\" + lot + "\\" + wafer ))
                except:
                    self.generating_ticket_done.emit(
                        str("coudn't seperated image for wafer " + job + "\\" + setup + "\\" + lot + "\\" + wafer))
        if self.stop_requested:
            self.generating_ticket_done.emit("process was stopped")
        else:
            self.generating_ticket_done.emit("all images was extracted")



class UI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.connect()

    def resizeEvent(self, event):
        # This function is called when the main window is resized
        # You can perform custom actions or update your UI here
        win_size = self.centralwidget.geometry().getRect()

        Height_factor=(win_size[3]/(self.Org_height-20)-1)/2 +1
        Width_factor=(win_size[2]/self.Org_width -1)/2 +1
        self.Org_height = win_size[3]
        self.Org_width = win_size[2]
        if self.open_flag:
            for obj in self.object_list:
                ref_h = obj.height()
                ref_w = obj.width()
                obj.resize(ref_h*Height_factor,ref_w*Width_factor)
                print(obj.objectName() +" resized to width:", self.width(), "height:", self.height())
        else:
            self.open_flag = True
        print("Main window resized to width:", self.width(), "height:", self.height())
        x=1
    def init(self):
        self.SR_folder= ""
        self.Procc_flag = False

    def connect(self):
        self.Choose_SR.clicked.connect(self.select_folder)
        self.Start.clicked.connect(self.select_folder)

    def select_folder(self):
        sender = self.sender().objectName()
        if sender == "Choose_SR":
            root = tk.Tk()
            root.withdraw()
            self.SR_folder = filedialog.askdirectory(title="select SR folder")
            self.label_SR.setText("Folder path: " + self.SR_folder)
        else:
            if not ((len(self.SR_folder) == 0)):
                if not self.Procc_flag:
                    self.Start.setText("Stop")
                    self.start_simulation()
                    self.Procc_flag = True
                else:
                    self.stop_worker()
                    self.Procc_flag = False

    def start_simulation(self):
        self.worker = Copy_Worker(self.SR_folder)
        self.worker.generating_ticket_done.connect(self.update_log_list)
        self.worker.start()

    def stop_worker(self):
        self.worker.stop()
        self.Start.setText("Start")

    def update_log_list(self,log_str):
        self.listWidget.addItem(log_str)
        self.listWidget.scrollToBottom()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    main_win=UI()
    main_win.show()

    app.exec_()