#!/usr/bin/python3

from smtplib import SMTP_SSL
import base64
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from template import templateMail


class SendMail():
    def __init__(self, freeSpace = '', data = {}):
        self.freeSpace = freeSpace
        self.data = data
        # Параметры письма
        self.mail_subj = 'hddDaemon: Мало свободного места!'  # заголовок письма

    def constructMessage(self):
        # формирование сообщения
        self.multi_msg = MIMEMultipart('alternative')
        self.multi_msg['From'] = self.data['mail_from']
        self.multi_msg['To'] = self.data['mail_to']
        self.multi_msg['Subject'] = self.mail_subj

        html = templateMail.my_template(self.freeSpace)

        msgFormat = MIMEText(html, 'html')
        self.multi_msg.attach(msgFormat)

        return self._sendMessageToMail()

    def _sendMessageToMail(self):
        # отправка
        smtp = SMTP_SSL()
        smtp.connect(self.data['smtp_server'])
        try:
            smtp.login(self.data['mail_from'], self.data['smpt_pass'])
        except Exception:
            print('Ошибка! Проверьте логин, пароль и адрес сервера для отправки')
            return False
        smtp.sendmail(self.data['mail_from'], self.data['mail_to'], self.multi_msg.as_string())
        smtp.quit()
        return True


if __name__ == '__main__':
    sendM = SendMail()
    sendM.constructMessage()





