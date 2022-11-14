from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from django.conf import settings
import urllib.request
from fpdf import FPDF

def send_mail(user_email,file_path, user_name, taskName, validationData,VRankingAlg,RocType,TupaType, scaletype, iterations, survivalRate,pk):
    # Create a multipart message.
    msg = MIMEMultipart()
    createPDF(taskName,validationData,VRankingAlg,RocType,TupaType,scaletype,iterations,survivalRate,pk)
    body_part = MIMEText('Hi '+ user_name+
                         '\nPyCR is finished processing your job. Your results are contained in the attached .zip file, and are also available for download from the pycr.dev website in your task list.\n'+
                         '\nPlease note that your results include in the pdf file attatched with this email. '+
                         '\n Thank you for using PyCR.'
                         '\n Please do not reply to this email.'
                         , 'plain')
    msg['Subject'] = "output"
    msg['From'] = "pycr@ualberta.ca"
    msg['To'] = user_email
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    file_msg_output = MIMEBase('application', 'zip')
    file_msg_pdf = MIMEBase('application', 'pdf')
    print(file_path)
    full_path_filename_output = 'https://' + 'pycr' + '.s3.us-east-2.amazonaws.com/' + file_path
    full_path_filename_pdf = 'static/images/featureSelection/temp/emailPDF/email_info'+str(pk)+'.pdf'
    zf_output = urllib.request.urlopen(full_path_filename_output)
    file_msg_output.set_payload(zf_output.read())
    file_msg_pdf.set_payload(open(full_path_filename_pdf,'rb').read())
    encoders.encode_base64(file_msg_output)
    encoders.encode_base64(file_msg_pdf)
    file_msg_output.add_header('Content-Disposition', 'attachment',
                   filename='output.zip')
    file_msg_pdf.add_header('Content-Disposition', 'attachment',
                   filename='task_detail.pdf')
    msg.attach(file_msg_output)
    msg.attach(file_msg_pdf)

    # Create SMTP object
    smtp_obj = smtplib.SMTP('smtp.gmail.com', port=587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login(user="pycr@ualberta.ca", password=settings.EMAIL_PSW)
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()


def runSendEmail(user_email, file_path,root_url,userName,taskName,isExternal, RankingAlg,rocType,tupaType,scaleType,iterations,survivalRate,pk):
    if isExternal:
        ValidationData = "with External Dataset"
    else:
        ValidationData = "Without External Dataset"
    send_mail(user_email, file_path, userName, taskName, ValidationData, RankingAlg, rocType, tupaType, scaleType, iterations,
              survivalRate,pk)

def createPDF(taskName, validationData, rankingAlgorithm, rocType, tupaType, scaleType, iterations, survivalRate,pk):

    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
    # create a cell
    pdf.cell(200, 10, txt = "Task Details",
            ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Task Name: ' + taskName,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Dataset: '+ validationData,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Variable Ranking Algorithm: ' + rankingAlgorithm,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Roc Type: '+ rocType,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Tupa Type: ' + tupaType,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt = 'Scale Type: ' + scaleType,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt ='How Many Iteration: ' + str(iterations),
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt ='Survival Rate: ' + str(survivalRate) ,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt ='Thank you for using PyCR. ' + str(survivalRate) ,
        ln = 2, align = 'C')
    pdf.cell(200, 10, txt ='Please do not reply to this email. ' + str(survivalRate) ,
        ln = 2, align = 'C')
    # save the pdf with name .pdf
    outputPath = "static/images/featureSelection/temp/emailPDF/email_info"+str(pk)+".pdf"
    pdf.output(outputPath,'F')  


