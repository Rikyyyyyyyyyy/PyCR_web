from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase

def send_mail(user_email,file_path, user_name, taskName, validationData,VRankingAlg,RocType,TupaType, scaletype, iterations, survivalRate):
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText('Hi '+ user_name+
                         '\nhere is the output from PyCR, please do not reply.\n'+
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
                         'How Many Iteration: ' + str(iterations)+ '\n' +
                         'Survival Rate: ' + str(survivalRate) + '\n'
                         , 'plain')
    msg['Subject'] = "output"
    msg['From'] = "pycr@ualberta.ca"
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
    smtp_obj.login(user="pycr@ualberta.ca", password='Tmic2022tmic')
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()


def runSendEmail(user_email, file_path,root_url,userName,taskName,isExternal, RankingAlg,rocType,tupaType,scaleType,iterations,survivalRate):
    url = str(root_url) + file_path
    if isExternal:
        ValidationData = "with External Dataset"
    else:
        ValidationData = "Without External Dataset"
    send_mail(user_email, url, userName, taskName, ValidationData, RankingAlg, rocType, tupaType, scaleType, iterations,
              survivalRate)

