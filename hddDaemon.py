#!/usr/bin/python3
import os
import subprocess
import re
import platform
import ctypes
import time
from daemon import runner


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.basedir = "/home/"

    def run(self):
        print('PID запущенного процесса - {}'.format(os.getpid()))
        while True:
            # strOut = str(subprocess.check_output("du -sk ~/workspace", shell=True))
            # sizeFolder = re.match(r'..(\d*).', strOut).group(1)

            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None,
                                                           ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                freeSpace = os.statvfs('/home').f_bavail * os.statvfs('/home').f_bsize
                print('Количество свободного места = {}Кб'.format(freeSpace))
                print('Количество свободного места = {}Гб'.format(round(freeSpace/1024**3, 2)))

            # print('!--> ', result2.group(1))
            # print('==> ', result)
            # print('Размер папки = {}Кб'.format(int(sizeFolder)))
            time.sleep(10)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
