import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class EmailHandler:
    def __init__(self):
        self.__email_source = TradeBotUtils.get_email_source()
        self.__email_source_password = TradeBotUtils.get_email_source_password()
        self.__email_target = TradeBotUtils.get_email_target()

    def create_message(self, subject, email_message):
        message = MIMEMultipart()
        message['From'] = self.__email_source
        message['To'] = self.__email_target
        message['Subject'] = subject
        message.attach(MIMEText(email_message, 'plain'))
        return message

    def create_attachment(self, file_path):
        with open(file_path, "rb") as f:
            attachment = MIMEBase('applications', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition',
                                  'attachment; filename=%s' % os.path.basename(file_path))
        return attachment

    def send_email_with_attachment(self, subject, email_message, file_paths):
        message = self.create_message(subject, email_message)
        for file_path in file_paths:
            message.attach(self.create_attachment(file_path))
        self.send_email(message)

    def send_email_message(self, subject, email_message):
        message = self.create_message(subject, email_message)
        self.send_email(message)

    def send_email(self, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.__email_source, self.__email_source_password)
        text = message.as_string()
        server.sendmail(self.__email_source, self.__email_target, text)
        server.quit()
        print('---Email Sent---\n\n')
