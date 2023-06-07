import hashlib
import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

email_sender = os.getenv('email_sender')
email_password = os.getenv('email_password')


def send_new_password_email(reciver, password):

    subject = 'New Password for ComunicationLTD'
    body = """
    the new password is:
    """ + password

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = reciver
    em['Subject'] = subject
    em.set_content(body)

    contex = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contex) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, reciver, em.as_string())