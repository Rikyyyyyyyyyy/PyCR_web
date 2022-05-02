import threading
from python_scripts.Feature_selection import PyCR
from faker import Faker
import shutil
from python_scripts import sent_email
fake = Faker()


class PyCRThread(Thread):
    def __init__(self,isExternal, splitRatio, rocType, tupaType, isMotabo, motabo_url, sample_url, class_url, sampleName_url, variableName_url, scaleType, iterations, survivalRate, rankingAlgorithm, vipComponent, pk,task,isSendEmail,cur_user, base_dir):
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
    def run(self):
        try:
            PyCR.runPyCR(self.isExternal, self.splitRatio, self.rocType, self.tupaType, self.isMotabo, self.motabo_url, self.sample_url, self.class_url, self.sampleName_url, self.variableName_url, self.scaleType, self.iterations, self.survivalRate, self.rankingAlg, self.nComp, self.pk)
            shutil.make_archive('static/images/featureSelection/temp/zipOutput/output' + str(self.task.pk), "zip",
                                'static/images/featureSelection/temp/output/', 'output' + str(self.task.pk))
            self.task.project_output.name = '/featureSelection/temp/zipOutput/output' + str(self.task.pk) + ".zip"
            self.task.save()
            if self.isSentEmail:
                # sent_mail_out = run([sys.executable,
                #            '//Users//wenwenli//Desktop//TMIC//PyCRWEB//python_scripts//sent_email.py',
                #           current_user.email,'/static/images/featureSelection/temp/zipOutput/output'+str(task.pk)+'.zip', settings.BASE_DIR,current_user.username,task.task_name, task.isExternal, task.rankingAlgorithm, task.rocType, task.tupaType, task.scaleType,str(task.iterations),str(task.survivalRate)], shell=False, stdout=PIPE)
                sent_email.runSendEmail(self.cur_user.email,'/static/images/featureSelection/temp/zipOutput/output'+str(self.task.pk)+'.zip',self.base_dir,self.cur_user.username,self.task.task_name, self.task.isExternal, self.task.rankingAlgorithm, self.task.rocType, self.task.tupaType, self.task.scaleType,self.task.iterations,self.task.survivalRate)
        except Exception as e:
            print(e)