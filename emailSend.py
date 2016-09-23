#!/usr/bin/python3

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail():
    def __init__(self, freeSpace = ''):
        self.freeSpace = freeSpace
        # Параметры письма
        self.mail_from = 'khorark@mail.ru'
        self.mail_to = 'khorark@ya.ru'
        self.mail_subj = 'MAS Project: Мало свободного места!'  # заголовок письма
        # Параметры SMTP-сервера
        self.smtp_server = 'smtp.mail.ru'
        self.smtp_user = self.mail_from  # пользователь smtp
        self.smtp_pwd = ''  # пароль smtp

    def constructMessage(self):
        # формирование сообщения
        self.multi_msg = MIMEMultipart('alternative')
        self.multi_msg['From'] = self.mail_from
        self.multi_msg['To'] = self.mail_to
        self.multi_msg['Subject'] = self.mail_subj

        html = """\
        <html>
          <head></head>
          <body>
            <p>
                <h3>На сервере осталось мало свободно места!</h3>
                <p>Пожалуйста, примите какие-либо меры, или ваш сервер упадет в ближайшее время ;-( </p>
                <p><b>Ориентировачное оставшееся место  = {} Гб</b></p>
            </p>
          </body>
        </html>
        """.format(self.freeSpace)

        msgFormat = MIMEText(html, 'html')
        self.multi_msg.attach(msgFormat)

        return self._sendMessageToMail()

    def _sendMessageToMail(self):
        # отправка
        smtp = SMTP_SSL()
        smtp.connect(self.smtp_server)
        try:
            smtp.login(self.mail_from, self.smtp_pwd)
        except Exception:
            print('Ошибка! Проверьте логин, пароль и адрес сервера для отправки')
            return False
        smtp.sendmail(self.mail_from, self.mail_to, self.multi_msg.as_string())
        smtp.quit()
        return True


if __name__ == '__main__':
    sendM = SendMail()
    sendM.constructMessage()





