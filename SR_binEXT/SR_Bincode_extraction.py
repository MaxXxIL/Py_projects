import shutil
import subprocess
import os
import pandas as pd
import argparse
import xmltodict
import configparser
from PIL import Image
def SR_Bincode_extraction(path):
    doc = Read_XML_file('configuration.xml')
    config = configparser.ConfigParser()
    #deleteeeeeee
    path = "F:\Analyzation\Wolfspeed Carsem\SR\Data-03102024\Wafers\HC346806CIF5_Version1"
    destination_path = doc["root"]["Output_folder_name"]
    Max_yield =int( doc["root"]["Max_yield"])
    Max_defects =int( doc["root"]["Max_defects"])
    path_list = path.split(";")
    for SR in path_list:
        str_len = len(SR)
        if str_len > 0:
            SR_path = SR.replace('/', '\\')
            tmp_str = path.split("\\")
            job = tmp_str[-4]
            setup = tmp_str[-3]
            lot = tmp_str[-2]
            config.read(SR + "\Scanlog.ini")
            try:
                print("starting loading df")
                print(str(config["General"]["Yield"]))
                if (float(config["General"]["Yield"]) > Max_yield):
                    print("Yield good")
                    if (int(config["General"]["DefectsNum"])<Max_defects):
                        print(str(config["General"]["DefectsNum"]))
                        Machine = config["General"]["Machine"]
                        cmd = 'ExportAdc.exe -srp ' '"' + SR_path + '"' ' /cld:-1 /cd:-1 /tm:surface=0,chipping=1,prob=2'
                        subprocess.run(cmd, shell=True, check=True)
                        print("Executable ran successfully.")
                        data_frame = pd.read_csv(SR + "\\ADC\\Surface2Bump.csv")
                        print("Surface2Bump loaded succesfully")
                        Oclass_df = data_frame[["ImageName", " OClass","ImageX","ImageY"]].copy()
                        for index,row in Oclass_df.iterrows():
                            img_name = row["ImageName"]
                            Oclass = row[" OClass"]
                            if not(os.path.exists(destination_path + "\\" + Machine + "\\" + job + "\\" + setup + "\\"  + str(Oclass))):
                                os.makedirs(destination_path + "\\" + Machine + "\\" + job + "\\" + setup + "\\"  + str(Oclass))
                            if img_name=="34979.70433.t.2.jpeg":
                                x=1
                            T_img = Image.open(SR + "\\" + img_name)
                            if len(T_img.getbands())==1:
                                cropped = Crop_Im(T_img, row["ImageX"], row["ImageY"])
                                cropped.save(destination_path + "\\" + Machine + "\\" + job + "\\" + setup + "\\" + str(
                                                Oclass) + "\\" + img_name )
                            else:
                                shutil.copy(SR + "\\" + img_name , destination_path + "\\" + Machine + "\\" + job + "\\" + setup + "\\"  + str(Oclass))
            except Exception as e:
                print("Error accured:", e)

def Read_XML_file(path):
    with open(os.path.normpath(path)) as fd:
        doc = xmltodict.parse(fd.read())
    return doc
    fd.close()

def Crop_Im(img,x,y):
    width, height = img.size
    top, bottom, left, right = (int(height - (height - y)), int(height*2 - (height - y)),int(width -(width - x)), int(height*2 - (width - x)))
    padding_color = (0, 0, 0)
    padded_image = Image.new(mode="RGB", size=(height*2, width*2), color=padding_color)
    padded_image.paste(img, box=(int(width/2),int(height/2)))
    cropped_img = padded_image.crop((left, top, right, bottom))
    return cropped_img
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arg1", type=str, help="Argument 1")
    args = parser.parse_args()
    SR_Bincode_extraction(args.arg1)