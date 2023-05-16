import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from create import SENDER_EMAIL, PASSWORD_EMAIL, RECIPIENT_EMAIL


def send_email(subject='TelegramBot',
               message='message from telegrambot',
               attach_file=True):
    msg = MIMEMultipart()

    msg['From'] = SENDER_EMAIL
    password = PASSWORD_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attach_file:
        part = MIMEBase('application', "octet-stream")
        with open('../logconfig.log', 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename={}'.format('logconfig.log'))
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com: 465') as smtp:
        #with smtplib.SMTP('smtp.gmail.com: 587') as smtp:
        smtp.login(SENDER_EMAIL, PASSWORD_EMAIL)
        smtp.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        #server.login(msg['From'], password)
        #server.sendmail(msg['From'], msg['To'], msg.as_string())


if  __name__ == '__main__':
    send_email()
