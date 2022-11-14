import threading
from python_scripts.Feature_selection import PyCR_2nd as PyCR
from faker import Faker
import shutil
import boto3
from django.conf import settings
import os
from python_scripts import sent_email
import datetime
fake = Faker()
class PyCRThread(threading.Thread):
    def __init__(self, isExternal, splitRatio, rocType, tupaType, isMotabo, motabo_url, sample_url, class_url, sampleName_url, variableName_url,external_type, ex_isMotabo, ex_motabo_url, ex_sample_url, ex_class_url, ex_sampleName_url, ex_variableName_url, scaleType, normType, iterations, survivalRate, rankingAlgorithm, vipComponent, pk,task,isSendEmail,cur_user, base_dir,task_name):
        self.isExternal = isExternal
        self.splitratio = splitRatio
        self.rocType = rocType
        self.tupaType = tupaType
        self.isMotabo = isMotabo
        self.motabo_url = motabo_url
        self.sample_url = sample_url
        self.class_url = class_url
        self.sampleName = sampleName_url
        self.VariableName = variableName_url
        self.scaleType = scaleType
        self.iterations = iterations
        self.survivalRate = survivalRate
        self.rankingAlg = rankingAlgorithm
        self.nComp = vipComponent
        self.pk = pk
        self.task = task
        self.isSentEmail = isSendEmail
        self.cur_user = cur_user
        self.base_dir = base_dir
        self.task_name = task_name
        self.external_type = external_type
        self.ex_isMotabo =  ex_isMotabo
        self.ex_motabo_url = ex_motabo_url
        self.ex_sample_url = ex_sample_url
        self.ex_calss_url = ex_class_url
        self.ex_sampleName_url = ex_sampleName_url
        self.ex_variableName = ex_variableName_url
        self.normType = normType
        
        threading.Thread.__init__(self)


    def run(self):
        # try:
            s3 = boto3.resource('s3')
            BUCKET = "pycr"
            PyCR.runPyCR(self.isExternal, self.splitratio, self.rocType, self.tupaType, self.isMotabo, self.motabo_url, self.sample_url, self.class_url, self.sampleName, self.VariableName,self.external_type, self.ex_isMotabo, self.ex_motabo_url, self.ex_sample_url, self.ex_calss_url, self.ex_sampleName_url, self.ex_variableName, self.scaleType,self.normType, self.iterations, self.survivalRate, self.rankingAlg, self.nComp, self.pk)
            os.rename( 'static/images/featureSelection/temp/output/'+ 'output' + str(self.task.pk), 'static/images/featureSelection/temp/output/'+ 'output_' + self.task_name)
            shutil.make_archive('static/images/featureSelection/temp/zipOutput/output_' + self.task_name, "zip",
                                 'static/images/featureSelection/temp/output/'+ 'output_' + self.task_name)
            self.task.project_output.name = "featureSelection/temp/zipOutput/output_"+ self.task_name + ".zip"
            folder_name = settings.MEDIA_ROOT +'/featureSelection/temp/output/'+ 'output_' + self.task_name
            zipName = settings.MEDIA_ROOT + '/featureSelection/temp/zipOutput/output_' + self.task_name + ".zip"
            s3.Bucket(BUCKET).upload_file(zipName, "featureSelection/temp/zipOutput/output_"+ self.task_name + ".zip")
            shutil.rmtree(folder_name)
            os.remove(zipName)
            if self.isSentEmail:
                sent_email.runSendEmail(self.cur_user.email,'featureSelection/temp/zipOutput/output_'+ self.task_name+'.zip',self.base_dir,self.cur_user.username,self.task.task_name, self.task.isExternal, self.task.rankingAlgorithm, self.task.rocType, self.task.tupaType, self.task.scaleType,self.task.iterations,self.task.survivalRate,self.pk)
                # sent_email.runSendEmail(self.cur_user.email,'featureSelection/temp/zipOutput/output298'+'.zip',self.base_dir,self.cur_user.username,self.task.task_name, self.task.isExternal, self.task.rankingAlgorithm, self.task.rocType, self.task.tupaType, self.task.scaleType,self.task.iterations,self.task.survivalRate)
            generate_time = datetime.datetime.now()
            self.task.output_time = generate_time
            self.task.save()

            # return False
        # except Exception as e:
        #     print("ERROR MESSAGE")
        #     erro_message = str(e)
        #     print(e)
        #     self.task.erro_message = erro_message[99:]
        #     self.task.save()