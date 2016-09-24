#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2016 Arkadiy
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import platform
import ctypes
import time
import json
import re
from daemon import runner
from emailSend import SendMail
import base64


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.path = 'setting.json'

    def checkFileSettings(self):
        try:
            self.data = json.load(open(self.path))
            # Проверка пароля пользователя
            if (self.data['smpt_pass'] == ''):
                self.data['smpt_pass'] = input('Введите пароль от почты: \n')
            else:
                self.data['smpt_pass'] = base64.b64decode(self.data['smpt_pass'])
                self.data['smpt_pass'] = self.data['smpt_pass'].decode('utf-8')
        except FileNotFoundError:
            mes = input('Файл с настройками не был найден! Необходима первоначальная настройка программы. Настроить сейчас? y/n ')
            if mes == 'y':
                self.createSettingFile()
            elif mes == 'n':
                exit(0)
            else:
                self.checkFileSettings()
        except TypeError:
            print('Неизвестный тип файла. Пожалуйста выполните настройку заново')

    def createSettingFile(self):
        print('Вас приветсвует мастер первоначальной настройки скрипта!')
        data = {}
        data['basedir'] = input('Введите полный путь к директории/устройству для отслеживания свободного места.\n')
        if (os.path.exists(data['basedir']) == False):
            print('Такой директории не существует!')
            self.createSettingFile()
            return
        data['min_size'] = input('Введите критический объем, при котором будет отправлено сообщение (в Гб):\n')
        data['time_update'] = input('Введите интервал обновления данных для проверки (в секундах)\n')
        data['mail_from'] = input('Введи почтовый адрес отправителя:\n')
        reg_smtp_serv = '.+@(.+)\..+'
        if (re.match(reg_smtp_serv, data['mail_from']).group(1)):
            smtp_serv = re.match(reg_smtp_serv, data['mail_from']).group(1)
            if smtp_serv == 'mail':
                data['smtp_server'] = 'smtp.mail.ru'
            elif smtp_serv == 'ya' or 'yandex':
                data['smtp_server'] = 'smpt.yandex.com'
            elif smtp_serv == 'gmail':
                data['smtp_server'] = 'smtp.googlemail.com'
            else:
                data['smtp_server'] = input('Введи почтовый smtp сервер вручную: \n')
        else:
            print('Вы ввели некорректный email!')
            exit(1)

        data['mail_to'] = input('Введите почтовый адрес получателя:\n')
        # q = input('Хотите сохранить пароль от почты в файл? y/n ')
        # if q == 'y':
        data['smpt_pass'] = input('Введите пароль от почты: \n')
        data['smpt_pass'] = base64.b64encode(bytes(data['smpt_pass'], "utf-8"))
        data['smpt_pass'] = data['smpt_pass'].decode('utf-8')
        # else:
        #     data['smpt_pass'] = ''

        json.dump(data, open(self.path, 'w'))
        print('Файл с настройкам успешно создан! Пожалуйста перезапустите программу')
        exit(0)

    def run(self):
        while True:
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.data['basedir']), None, None,
                                                           ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                freeSpace = os.statvfs('/home').f_bavail * os.statvfs(self.data['basedir']).f_bsize
                freeSpaceMb = round(freeSpace/1024**2, 2)
                freeSpaceGb = round(freeSpace/1024**3, 2)
                if (freeSpaceGb < int(self.data['min_size'])):
                    if (SendMail(freeSpaceGb, self.data).constructMessage() == False):
                        print('Демон остановлен')
                        return

            time.sleep(int(self.data['time_update']))


app = App()
app.checkFileSettings()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
