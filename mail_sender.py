import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import os
from dotenv import load_dotenv

load_dotenv()


def send_mail(sender, user_email, date, filepath = None):

    sender_mail = os.environ['sender_mail']
    reciever_mail = user_email

    # Message Head
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] = reciever_mail
    message['Subject'] = f"Financial Analysis for Stocks on {date}"

    # Email Body 
    body = f'''Hi There,\n\n\
The Automated Financial Analysis of {date} for the top 3 tech stocks.\n\n\
Please find the attachment excel file.\n\n\
Regards,\n\
{sender}'''
    message.attach(MIMEText(body, 'plain'))

    # Opening the Excel file
    excel_file = filepath
    attachment = open(excel_file, 'rb')

    # Creating the attachment part
    excel_part = MIMEBase('application', 'octet-stream')
    excel_part.set_payload((attachment).read())
    encoders.encode_base64(excel_part)
    excel_part.add_header('Content-Disposition', "attachment; filename= " + excel_file)

    # Attach the Excel file to the email
    message.attach(excel_part)

    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ['smtp_username']
    smtp_password = os.environ['smtp_password']

    # Creating an SMTP connection
    smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
    
    try:
        smtp_obj.starttls()
        smtp_obj.login(smtp_username, smtp_password)
    except Exception as e:
        print("SMTP Error: ", e)

    # Sending the email
    smtp_obj.sendmail(sender_mail, reciever_mail, message.as_string())

    # Closing the SMTP connection
    smtp_obj.quit()