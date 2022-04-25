from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import sys
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
import zipfile

def send_mail(user_email,file_path, user_name, taskName, validationData,VRankingAlg,RocType,TupaType, scaletype, iterations, survivalRate):
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText('Hi '+ user_name+
                         '\n  here is the output from PyCR, please do not reply.\n'+
                         '\n'+
                         '\n'+
                         '\n'+
                         '################### Details ################\n'+
                         'Task Name: ' + taskName + '\n'+
                         'Dataset: '+ validationData+ '\n'+
                         'Variable Ranking Algorithm: ' + VRankingAlg + '\n'+
                         'Roc Type: '+ RocType + '\n'+
                         'Tupa Type: ' + TupaType + '\n' +
                         'Scale Type: ' + scaletype + '\n' +
                         'How Many Iteration: ' + iterations + '\n' +
                         'Survival Rate: ' + survivalRate + '\n'
                         , 'plain')
    msg['Subject'] = "output"
    msg['From'] = "wenwenli.ws@gmail.com"
    msg['To'] = user_email
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    file_msg = MIMEBase('application', 'zip')
    zf = open(file_path, 'rb')
    file_msg.set_payload(zf.read())
    encoders.encode_base64(file_msg)
    file_msg.add_header('Content-Disposition', 'attachment',
                   filename='output.zip')
    msg.attach(file_msg)

    # Create SMTP object
    smtp_obj = smtplib.SMTP('smtp.gmail.com', port=587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login(user="wenwenli.ws@gmail.com", password='Li704647903')
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()

def main():
    user_email = sys.argv[1]
    file_path = sys.argv[2]
    root_url = sys.argv[3]
    userName = sys.argv[4]
    taskName = sys.argv[5]
    isExternal = sys.argv[6]
    RankingAlg = sys.argv[7]
    rocType = sys.argv[8]
    tupaType = sys.argv[9]
    scaleType = sys.argv[10]
    iterations = sys.argv[11]
    survivalRate = sys.argv[12]

    url = root_url + file_path
    if isExternal:
        ValidationData = "with External Dataset"
    else:
        ValidationData = "Without External Dataset"
    send_mail(user_email, url,userName,taskName,ValidationData, RankingAlg,rocType,tupaType,scaleType,iterations,survivalRate)
main()
