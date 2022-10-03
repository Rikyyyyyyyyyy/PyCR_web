import threading
from python_scripts.reconstruction import reconstructionMain
from faker import Faker
import shutil
import boto3
from django.conf import settings
import os
from python_scripts import sent_email
fake = Faker()
class reconstructThread(threading.Thread):
    def __init__(self, inputFile, cur_user, base_dir,pk,task,dir):
        self.inputFile = inputFile
        self.cur_user = cur_user
        self.base_dir = base_dir
        self.pk = pk
        self.task = task
        self.homePath = dir
        threading.Thread.__init__(self)

    def run(self):
        # try:
            s3 = boto3.resource('s3')
            BUCKET = "pycr"
            reconstructionMain.run1dreconstruct(self.inputFile,self.pk,self.homePath)
            ouput_path = 'static/images/reconstruct/output/output'+str(self.task.pk)+'.png'
            temp_path = 'static/images/reconstruct/temp/temp'+str(self.task.pk)+'MatrixOutput.csv'
            temp_input_path = 'static/images/reconstruct/temp_input/temp_input'+str(self.task.pk)+'.csv'
            self.task.outputFile.name = "others/1dreconstruct/outputs/output"+ str(self.task.pk) + ".png"
            s3.Bucket(BUCKET).upload_file(ouput_path, "others/1dreconstruct/outputs/output"+ str(self.task.pk) + ".png")
            self.task.save()
            os.remove(ouput_path)
            os.remove(temp_path)
            os.remove(temp_input_path)
            # return False
        # except Exception as e:
        #     print("ERROR MESSAGE")
        #     erro_message = str(e)
        #     print(e)
        #     self.task.erro_message = erro_message
        #     self.task.save()