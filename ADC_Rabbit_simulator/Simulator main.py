import os
import sys
import shutil
import time
from tkinter import messagebox, filedialog
from ADC_ticket_simulator import Ui_MainWindow
import xmltodict
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem ,QVBoxLayout
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QMetaObject, pyqtSignal


class Copy_Worker(QThread):
    generating_ticket_done = pyqtSignal(str)  # Signal to indicate the comparison is done
    stop_requested = pyqtSignal(bool)
    def __init__(self,SR_path,Ticket_path,Iterations,delay):
        super(Copy_Worker,self).__init__()
        self.SR_path = SR_path
        self.Ticket_path = Ticket_path
        self.Iterations = Iterations
        self.delay = delay
        self.stop_requested = False

    def run(self):
        for n,i in enumerate(range(self.Iterations)):
            if self.stop_requested:
                break
            Lot_list = os.listdir(self.SR_path)
            for lot in Lot_list:
                if self.stop_requested:
                    break
                wafer_list = os.listdir(self.SR_path + "\\" + lot)
                for wafer in wafer_list:
                    if self.stop_requested:
                        break
                    temp_string = self.SR_path.split('/')
                    job = temp_string[-2]
                    setup = temp_string[-1]
                    source_folder = self.SR_path + '/' + lot + '/' + wafer
                    destination_folder = self.Ticket_path + "/scanresults/" + job + "/" + setup + "/" + lot +"_" + str(n) + '/' + wafer
                    ticket_string = job + "|" + setup + "|" + lot + "_" + str(n) + "|" + wafer
                    xml_name = job + "_" + setup + "_" + lot + "_" + str(n) + "_" + wafer
                    self.copy_wafer(destination_folder,source_folder,ticket_string,xml_name)
                    self.generating_ticket_done.emit(str("Ticket generated for msg ->" + ticket_string))
                    time.sleep(self.delay)
        self.stop_requested = True
    def stop(self):
        self.stop_requested = True
        self.generating_ticket_done.emit("Worker have been stopped")

    def Read_XML_file(self,path):
        with open(os.path.normpath(path + '\\ticket_template.xml')) as fd:
            doc = xmltodict.parse(fd.read())
        return doc
        fd.close()

    def save_XML_file(self,path,file_name):
       with open(os.path.normpath(path + '/' + file_name + ".xml"),'w') as fd:
            doc = xmltodict.unparse(self.Xml_dict, pretty=True)
            fd.write(doc)
            fd.close()
            os.rename(path + '/' + file_name + ".xml", path + '/' + file_name + ".tck")

    def copy_wafer(self, destination_folder,source_folder,ticket_string,xml_name):
        self.Xml_dict = self.Read_XML_file(os.getcwd())
        self.Xml_dict['TicketData']['ParamValueLine'] =ticket_string
        shutil.copytree(source_folder, destination_folder)
        self.save_XML_file(self.Ticket_path + '/Tickets',xml_name)

class UI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.connect()

    def init(self):
        self.SR_folder= ""
        self.ticket_folder = ""

        self.Procc_flag = False
    def connect(self):
        self.Choose_SR.clicked.connect(self.select_folder)
        self.Choose_ticket.clicked.connect(self.select_folder)
        self.Start.clicked.connect(self.select_folder)

    def select_folder(self):
        sender = self.sender().objectName()
        if sender == "Choose_SR":
            self.SR_folder = filedialog.askdirectory(title="select SR folder")
            self.label_SR.setText("Folder path: " + self.SR_folder)
        elif sender == "Choose_ticket":
            self.ticket_folder = filedialog.askdirectory(title="select ticket folder")
            self.label_Ticket.setText("Folder path: " + self.ticket_folder)
        else:
            if not ((len(self.SR_folder) == 0) and (len(self.ticket_folder) == 0)):
                if not self.Procc_flag:
                    self.Start.setText("Stop")
                    self.start_simulation()
                    self.Procc_flag = True
                else:
                    self.stop_worker()

    def start_simulation(self):
        self.worker = Copy_Worker(self.SR_folder,self.ticket_folder,self.spinBox.value(),self.spinBox_delay.value())
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