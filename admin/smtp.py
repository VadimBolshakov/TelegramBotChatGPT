import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from create import SENDER_EMAIL, PASSWORD_EMAIL, RECIPIENT_EMAIL
from admin.logsetting import logger


def send_email(subject='TelegramBot',
               message='Message from telegrambot. ',
               file='../logconfig.log',
               attach_file=True):
    msg = MIMEMultipart()

    msg['From'] = SENDER_EMAIL
    password = PASSWORD_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attach_file:
        try:
            part = MIMEBase('application', 'octet-stream')
            with open(file, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}'.format('logconfig.log'))
            msg.attach(part)
        except FileNotFoundError as e:
            logger.exception(f'Error attach file: {str(e)}')
            msg.attach(MIMEText(f'Error attach file: {str(e)}', 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com: 587') as smtp:
            # with smtplib.SMTP_SSL('smtp.gmail.com: 465') as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SENDER_EMAIL, password)
            smtp.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            logger.info(f'Email send to {RECIPIENT_EMAIL}')

    except smtplib.SMTPAuthenticationError as e:
        logger.exception(f'Error send email: {str(e)}')
    except smtplib.SMTPSenderRefused as e:
        logger.exception(f'Error send email: {str(e)}')
    except smtplib.SMTPRecipientsRefused as e:
        logger.exception(f'Error send email: {str(e)}')
    except smtplib.SMTPConnectError as e:
        logger.exception(f'Error send email: {str(e)}')
    except TimeoutError as e:
        logger.exception(f'Error send email: {str(e)}')


if __name__ == '__main__':
    send_email()
