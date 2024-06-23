
from PyQt5 import QtGui, Qt
from product_editor import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QListWidget, QLabel, QListView, QMessageBox, QTreeView, QInputDialog
from PyQt5.Qt import QStandardItemModel ,QStandardItem
from PyQt5.QtGui import QPalette, QColor ,QBrush
from PyQt5.QtCore import Qt
import os.path
import sys
import xmltodict
import shutil
from datetime import datetime




class my_window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_params()
        self.emgime_image_type=('color','color_ref','color_bw','bw','bw_ref','bw2','bw2_ref','ici','ici_ref')
        self.engine_convert=('no_conversion','color_to_bw','bw_to_color')
        self.engine_types = ('simple', 'join_2')
        self.architectures = ('resnet18', 'resnet34', 'resnet50', 'resnet152', 'alex_net', 'vgg16', 'googlenet', 'squeezenet', 'densenet', 'inception', 'shufflenet', 'mobilenet', 'resnext')
        self.comboBox.activated.connect(self.init_product)
        self.Image_type.activated.connect(self.change_image_type)
        self.comboBox_Engine.activated.connect(self.change_engine)
        self.model_trial.activated.connect(self.change_model_trial)
        self.Set_parameters.clicked.connect(self.edit_dict)
        self.add_active_engine.clicked.connect(self.add_active_engine_to_list)
        self.Remove_active_eng.clicked.connect(self.remove_active_engine)

    def init_product(self):
        #-------------------upload product xml ----------------#
        try:
            product = self.comboBox.currentText()
            self.Xml_dict = self.Read_XML_file(self.products_list[product])
        except:
            self.Xml_dict = self.Read_XML_file(os.getcwd())
        self.root_element = self.Xml_dict['root']
        self.engines_list=[]
        for engine in self.root_element['engines']['engine']:
            if type(engine) is dict:
                self.engines_list.append(engine['name'])
            else:
                self.engines_list.append(self.root_element['engines']['engine']['name'])
                break;
        #------ get  xml high params ------#
        self.Version.setText(('Version: ' + self.root_element['version']['number']))
        self.Date.setText(('Date: ' + self.root_element['version']['date']))
        self.Date.setText(('Date: ' + self.root_element['version']['date']))
        self.plainTextEdit_2.setPlainText(self.root_element['config_folder_name'])
        self.plainTextEdit_3.setPlainText(self.root_element['product'])
        self.listWidget.clear()
        # ------ get  all engines list------#

        # ------ get  active engines ------#
        act_eng_str=self.root_element['active_engines']
        self.active_engines=[]
        try:
            active_engines = act_eng_str.split(';')
            for p in active_engines:
                self.active_engines.append(p)
            self.listWidget.addItems(self.active_engines)
        except:
             self.listWidget.addItems(self.root_element['active_engines'])
             self.active_engines.append(self.root_element['active_engines'])

        if self.root_element['generate']['generate_data_in_addition_to_factors'] == '1':
            self.radioButton.setChecked(1)
        # ------ extract engine params ------#
        image_element = self.root_element['input_image_properties']['image']
        self.im_type_dict={}
        im_type_l=[]
        if type(image_element) is not dict:
            for im_type in image_element:
                self.im_type_dict[im_type['image_type_name']] = [im_type['image_type_name'], im_type['size_w'], im_type['size_h'], im_type['max_offset_from_center']]
                im_type_l.append(im_type['image_type_name'])
        else:
            self.im_type_dict[image_element['image_type_name']] = [image_element['image_type_name'], image_element['size_w'], image_element['size_h'], image_element['max_offset_from_center']]
            im_type_l.append(image_element['image_type_name'])
        self.Image_type.clear()
        self.Image_type.addItems(im_type_l)
        self.update_image_type(self.im_type_dict[im_type_l[0]])
        self.debug.setChecked(int(self.root_element['process']['debug']))
        self.training_p.setPlainText(str(float(self.root_element['train']['training_percent'])*100))
        self.validation_p.setPlainText(str(float(self.root_element['train']['validation_percent']) * 100))
        self.max_epochs.setPlainText(self.root_element['train']['n_epochs_with_no_improvment'])
        self.engine_dict={}
        engines_l=[]
        engine_element = self.root_element['engines']['engine']
        if type(engine_element) is not dict:
            for eng in engine_element:
                self.engine_dict[eng['name']] = eng
                engines_l.append(eng['name'])
            self.update_engine(engine_element[0])
        else:
            self.engine_dict[engine_element['name']] = engine_element
            engines_l.append(engine_element['name'])
            self.update_engine(engine_element)
        self.engines_l = engines_l
        self.comboBox_Engine.clear()
        self.comboBox_Engine.addItems(engines_l)


    def init_params(self):
        try:
            self.products_list = self.search_products()
        except:
            self.products_list={}
            self.products_list['STAT_STM_M5'] = os.path.normpath(os.getcwd() + '\config1_STAT')
        self.comboBox.addItems(self.products_list)

    def search_products(self):
        list={}
        dir_path = os.path.normpath('C:/adc/configurations')
        product_dirs = os.listdir(dir_path)
        for dir in product_dirs:
            path_files= os.listdir(os.path.normpath(dir_path + '\\' + dir))
            xml_files = os.listdir(os.path.normpath(dir_path + '\\' + dir + '\\' + path_files[0]))
            valid_flag=1;
            xmls=['ADC_generate_training_Engines_Setup.xml' ,'ADC_Setup.xml']
            for file in xmls:
                if not file in xml_files:
                    valid_flag = 0
                    break
            if valid_flag:
                list[dir]=os.path.normpath(dir_path + '\\' + dir + '\\' + path_files[0])
        return list

    def Read_XML_file(self,path):
        with open(os.path.normpath(path + '\\ADC_generate_training_Engines_Setup.xml')) as fd:
            doc = xmltodict.parse(fd.read())
        return doc
        fd.close()

    def save_XML_file(self,path):
        currentDateAndTime = str(datetime.now()).split(' ')
        tmp = currentDateAndTime[1].split(':')
        d_ext = currentDateAndTime[0] + '_' + tmp[0] + '_' + tmp[1] + '_' + tmp[2][1:2]
        shutil.copy(os.path.normpath(path + '\\ADC_generate_training_Engines_Setup.xml'), os.path.normpath(path + '\\ADC_generate_training_Engines_Setup_' + d_ext + '.xml'))
        with open(os.path.normpath(path + '\\ADC_generate_training_Engines_Setup.xml'),'w') as fd:
            doc = xmltodict.unparse(self.Xml_dict, pretty=True)
            fd.write(doc)

    def change_engine(self):
        eng = self.comboBox_Engine.currentText()
        self.update_engine(self.engine_dict[eng])

    def change_model_trial(self):
        model_trial = self.model_trial.currentText()
        self.update_model_trial(self.trial_dict[model_trial])

    def change_image_type(self):
        product = self.Image_type.currentText()
        self.update_image_type(self.im_type_dict[product])

    def update_image_type(self ,image_element):
        self.Image_width.setPlainText(image_element[1])
        self.Image_height.setPlainText(image_element[2])
        self.Image_offset.setPlainText(image_element[3])

    def update_engine(self,eng):
        self.eng_num.setValue(int(eng['number']))
        type_name = self.Image_type_engine.currentText()
        indx = self.emgime_image_type.index(type_name)
        self.Image_type_engine.setCurrentIndex(indx)
        image_type_l=[]
        if len(eng['images']) == 1:
            image_type_l.append(eng['images']['image']['image_type_name'])
        else:
            for image in eng['images']['image']:
                image_type_l.append(image['image_type_name'])
        self.model_t_image_type.clear()
        self.model_t_image_type.addItems(image_type_l)
        indx = self.engine_convert.index(eng['images']['image']['convert_to'])
        self.Image_convert.setCurrentIndex(indx)
        self.Image_resize.setPlainText(eng['images']['image']['source_image_size_linked_to_minus_one'])
        if eng['images']['image']['roi_resize'] == '-1':
            self.roi_resize.setChecked(1)
        else:
            self.roi_resize.setChecked(0)
        self.roi_size.setPlainText(eng['images']['image']['roi_size'])
        self.translate_shift.setPlainText(eng['images']['image']['translate_shift'])
        if eng['images']['image']['smooth_image'] == '0':
            self.image_smooth.setChecked(0)
        else:
            self.image_smooth.setChecked(1)
        self.spinBox.setValue(int(eng['generate']['max_factor']))
        self.spinBox_2.setValue(int(eng['generate']['max_factor_exceeding_percentage']))
        self.doubleSpinBox_2.setValue(float(eng['generate']['unbalanced_allowed_ratio']))
        self.trial_dict = {}
        trial_l = []
        for model_trial in eng['train']['model_trial']:
            self.trial_dict[model_trial['name']] = model_trial
            trial_l.append(model_trial['name'])
        self.model_trial.clear()
        self.model_trial.addItems(trial_l)
        self.update_model_trial(eng['train']['model_trial'][0])
        self.Treeview_class(eng['classes'])

    def update_model_trial(self,model_t):
        indx = self.engine_types.index(model_t['engine_type'])
        self.engine_type.setCurrentIndex(indx)
        self.spinBox_3.setValue(int(model_t['batch_size']))
        if model_t['active'] == '1':
            self.active_trial.setChecked(1)
        else:
            self.active_trial.setChecked(0)
        sub_engine_l = []
        sub_engine_dict = {}
        if len(model_t['sub_engines']) == 1:
            sub_engine_l.append(model_t['sub_engines']['sub_engine']['image_type_name'])
            sub_engine_dict[model_t['sub_engines']['sub_engine']['image_type_name']] = model_t['sub_engines']
        else:
            for sub in model_t['sub_engines']:
                sub_engine_l.append(sub['sub_engine']['image_type_name'])
                sub_engine_dict[model_t['sub_engines']['sub_engine']['image_type_name']] = model_t['sub_engines'][
                    'sub_engine']
        self.sub_engine.clear()
        self.sub_engine.addItems(sub_engine_l)
        indx = self.architectures.index(sub_engine_dict[self.sub_engine.currentText()]['sub_engine']['model_type'])
        self.architecture.setCurrentIndex(indx)

        # self.architecture.setCurrentIndex(indx)
        learning_str = sub_engine_dict[self.sub_engine.currentText()]['sub_engine']['learning_rate']
        tmp_str = learning_str.split('lr')
        tmp_str = tmp_str[1].split('_')
        self.spinBox_4.setValue(float(tmp_str[0]))
        tmp_str2 = tmp_str[1].split('factor')
        self.spinBox_5.setValue(float(tmp_str2[1]))
        tmp_str3 = tmp_str[2].split('patience')
        tmp_str3 = tmp_str3[1].split('*')
        self.spinBox_6.setValue(int(tmp_str3[0]))
        self.spinBox_7.setValue(int(tmp_str3[1]))

    def Change_xml_params(self):
#--------------------------------------------update product params-------------------------------------------------#
        curr_product = self.root_element
        if self.radioButton.isChecked():
            curr_product['generate']['generate_data_in_addition_to_factors'] = '1'
        else:
            curr_product['generate']['generate_data_in_addition_to_factors'] = '0'
        image_types = curr_product['input_image_properties']['image']
        curr_image_type = self.Image_type.currentText()
        image_W = self.Image_width.toPlainText()
        image_H = self.Image_height.toPlainText()
        image_offset = self.Image_offset.toPlainText()
        if len(image_types) > 1:
            for i,im in enumerate(image_types):
                if im['image_type_name'] == curr_image_type:
                    curr_image_type = curr_product['input_image_properties']['image'][i]
                    break
        else:
            curr_image_type = curr_product['input_image_properties']['image']
        curr_image_type['size_w'] = image_W
        curr_image_type['size_h'] = image_H
        curr_image_type['max_offset_from_center'] = image_offset

        if self.debug.isChecked():
           curr_product['process']['debug'] = '1'
        else:
            curr_product['process']['debug'] = '0'





#-------------------------------------------- Load engine from dict--------------------------------------------------------------------------#
        engine_name = self.comboBox_Engine.currentText()
        for i,eng in enumerate(self.root_element['engines']['engine']):
            if eng['name'] == engine_name:
                indx1 = i
                break
        curr_engine = self.root_element['engines']['engine'][indx1]

#--------------------------------------------Upate generate parametes--------------------------------------------
        curr_engine['generate']['max_factor'] = self.spinBox.value()
        curr_engine['generate']['max_factor_exceeding_percentage'] = self.spinBox_2.value()
        curr_engine['generate']['unbalanced_allowed_ratio'] = self.doubleSpinBox_2.value()
        curr_engine['images']['image']['image_type_name'] =self.Image_type_engine.currentText()
        curr_engine['images']['image']['convert_to'] =  self.Image_convert.currentText()

        if self.Image_resize.toPlainText().isnumeric():
            curr_engine['images']['image']['source_image_size_linked_to_minus_one'] = self.Image_resize.toPlainText()

        if self.roi_resize.text() == 'Active ':
            curr_engine['images']['image']['roi_resize'] = '-1'
        else:
            curr_engine['images']['image']['roi_resize'] = '1'
        if self.roi_size.toPlainText().isnumeric():
            curr_engine['images']['image']['roi_size'] = self.roi_size.toPlainText()
        if self.translate_shift.toPlainText().isnumeric():
            curr_engine['images']['image']['translate_shift'] = self.translate_shift.toPlainText()
        if self.image_smooth.text() == 'Active ':
            curr_engine['images']['image']['smooth_image'] = '1'
        else:
            curr_engine['images']['image']['smooth_image'] = '0'



#--------------------------------------------Load trial model from dict------------------------------------------- ----
        trial_name = self.model_trial.currentText()
        for j,trial in enumerate(curr_engine['train']['model_trial']):
            if trial['name'] == trial_name:
                indx2 = j
                break
        curr_model_trial = curr_engine['train']['model_trial'][indx2]
        curr_model_trial['engine_type'] = self.engine_type.currentText()
        curr_model_trial['batch_size'] = str(self.spinBox_3.value())
        if self.active_trial.text() == 'Active ':
            curr_model_trial['active'] = '1'
        else:
            curr_model_trial['active'] = '0'
        sub_eng_name= self.sub_engine.currentText()
        sub_eng_len=len(curr_model_trial['sub_engines'])
        indx3 = None

#--------------------------------------------Load sub engine from dict--------------------------------------------
        if  sub_eng_len==1:
            sub_eng = curr_model_trial['sub_engines']['sub_engine']

        else:
            for m,sub_engine in enumerate(curr_model_trial['sub_engines']):
                if sub_engine['image_type_name'] == sub_eng_name:
                    indx3 = m
                    break
            sub_eng = curr_model_trial['sub_engines']['sub_engine'][indx3]
        sub_eng['model_type'] = self.architecture.currentText()
        sub_eng['image_type_name'] = self.model_t_image_type.currentText()
        sub_eng['learning_rate'] = 'ReduceLROnPlateau_lr' + str(self.spinBox_4.value()) + '_factor' + str(self.spinBox_5.value()) + '_patience' + str(self.spinBox_6.value()) + '*' + str(self.spinBox_7.value())
        if indx3 is not None:
            curr_model_trial['sub_engines']['sub_engine'][indx3] = sub_eng
        else:
            curr_model_trial['sub_engines']['sub_engine'] = sub_eng
        x=1

    def Treeview_class(self, class_dict):
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        for cls in class_dict['class']:
            class_A = QStandardItem(cls['name'])
            class_A.setFont(font)
            primitive_str = cls['primitive_class']
            try:
                primitive_classes= primitive_str.split(';')
                for cls_name in primitive_classes:
                    primitive_class_A = QStandardItem(cls_name)
                    red_brush = QBrush(Qt.darkGreen)
                    primitive_class_A.setData(red_brush, Qt.TextColorRole)
                    class_A.appendRow(primitive_class_A)
            except:
                primitive_class_A = QStandardItem(cls['primitive_class'])
                class_A.appendRow(primitive_class_A)
            rootNode.appendRow(class_A)


        self.treeView.setHeaderHidden(True)
        self.treeView.setModel(treeModel)
        self.treeView.expandAll()
        self.treeView.show()

    def edit_dict(self):
        self.Change_xml_params()
        product = self.comboBox.currentText()
        self.save_XML_file(self.products_list[product])
        QMessageBox.about(self,"Info msg","the file was saved")

    def remove_active_engine(self):
        try:
            eng_name = self.listWidget.currentItem().text()
            self.active_engines.remove(eng_name)
        except:
            QMessageBox.about(self, "Error msg", "please selects active engine to remove")
        if len(self.active_engines) == 1:
            self.root_element['active_engines'] = self.active_engines[0]
        else:
            tmp_str=''
            for eng in self.active_engines:
                if tmp_str == '':
                    tmp_str = eng
                else:
                    tmp_str = tmp_str + ';' + eng
            self.root_element['active_engines'] = tmp_str
        self.listWidget.clear()
        self.listWidget.addItems(self.active_engines)

    def add_active_engine_to_list(self):
        item, ok = QInputDialog.getItem(self, "Select files", "List of files", self.engines_l, 0, False)
        if ok == True:
            active_list = self.root_element['active_engines']
            active_list = active_list + ';' + item
            self.root_element['active_engines'] = active_list
        self.active_engines.append(item)
        self.listWidget.clear()
        self.listWidget.addItems(self.active_engines)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    main_win=my_window()
    main_win.show()
    app.exec_()