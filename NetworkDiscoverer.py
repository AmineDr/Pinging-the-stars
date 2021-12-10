from subprocess import Popen, PIPE
from threading import Thread
import ctypes
import time
import os


class Explorer:
    def __init__(self, prefix):
        self.prefix = prefix
        self.flushed = False
        if ctypes.windll.shell32.IsUserAnAdmin():
            os.system("arp -d")
            self.flushed = True
        self.tested = 0
        for x in range(255):
            Thread(target=self.ping_to_arp, args=(f"{prefix}{x}",)).start()
            time.sleep(.05)

        while self.tested < 255:
            pass
        self.command = Popen(["arp", "-a"], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.stdout = self.command.stdout.read().decode()

    def ping_to_arp(self, ip):
        Popen(["ping", f"{ip}", "-n", '1', "-l", '1'], shell=True)
        self.tested += 1

    def get_addresses(self):
        lines = self.stdout.split('\r\n')[3:]
        valid_lines = []
        addresses = []
        for x, y in enumerate(lines):
            if y.find(self.prefix) != -1:
                valid_lines.append(lines[x][2:])

        for x, y in enumerate(valid_lines):
            valid_lines[x] = y.split(" ")
        for x, y in enumerate(valid_lines):
            address = []
            for w, z in enumerate(y):
                if z != '':
                    address.append(valid_lines[x][w].replace('-', ':'))
            addresses.append(address)

        return addresses, self.flushed
