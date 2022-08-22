from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from django.conf import settings
import urllib.request
def send_mail(user_email,file_path, user_name, taskName, validationData,VRankingAlg,RocType,TupaType, scaletype, iterations, survivalRate):
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText('Hi '+ user_name+
                         '\nPyCR is finished processing your job. Your results are contained in the attached .zip file, and are also available for download from the pycr.dev website in your task list.\n'+
                         '\nPlease note that your results will be deleted from our servers in seven days. Details about this task are as follows:'+
                         '\n'+
                         '\n'+
                         '################### Details ################\n'+
                         'Task Name: ' + taskName + '\n'+
                         'Dataset: '+ validationData+ '\n'+
                         'Variable Ranking Algorithm: ' + VRankingAlg + '\n'+
                         'Roc Type: '+ RocType + '\n'+
                         'Tupa Type: ' + TupaType + '\n' +
                         'Scale Type: ' + scaletype + '\n' +
                         'How Many Iteration: ' + str(iterations)+ '\n' +
                         'Survival Rate: ' + str(survivalRate) + '\n' +
                         '\n Thank you for using PyCR.'
                         '\n Please do not reply to this email.'
                         , 'plain')
    msg['Subject'] = "output"
    msg['From'] = "pycr@ualberta.ca"
    msg['To'] = user_email
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    file_msg = MIMEBase('application', 'zip')
    full_path_filename = 'https://' + 'pycr' + '.s3.amazonaws.com/' + file_path
    zf = urllib.request.urlopen(full_path_filename)
    file_msg.set_payload(zf.read())
    encoders.encode_base64(file_msg)
    file_msg.add_header('Content-Disposition', 'attachment',
                   filename='output.zip')
    msg.attach(file_msg)

    # Create SMTP object
    smtp_obj = smtplib.SMTP('smtp.gmail.com', port=587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login(user="pycr@ualberta.ca", password=settings.EMAIL_PSW)
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()


def runSendEmail(user_email, file_path,root_url,userName,taskName,isExternal, RankingAlg,rocType,tupaType,scaleType,iterations,survivalRate):
    if isExternal:
        ValidationData = "with External Dataset"
    else:
        ValidationData = "Without External Dataset"
    send_mail(user_email, file_path, userName, taskName, ValidationData, RankingAlg, rocType, tupaType, scaleType, iterations,
              survivalRate)

