#!/usr/bin/python3
import os
import platform
import ctypes
import time
from daemon import runner
from emailSend import SendMail


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.basedir = "/home/"
        self.buf = 0

    def run(self):
        while True:
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None,
                                                           ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                self.buf += 1
                freeSpace = os.statvfs('/home').f_bavail * os.statvfs('/home').f_bsize
                freeSpaceGb = round(freeSpace/1024**3, 2)
                print('Количество свободного места = {}Кб'.format(freeSpace))
                print('Количество свободного места = {}Гб'.format(freeSpaceGb))
                if (self.buf == 2):
                    print('Отправка письма!')
                    SendMail(freeSpaceGb).constructMessage()

            time.sleep(10)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
