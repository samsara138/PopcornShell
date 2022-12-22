# PopcornShell
A simple python reverse shell project

## Introduction
The attacker host a server, await for the victim to execute the file

The victim file will constantly try to connect to the specified server.

Once a connection is established, the attacker can send commands to the victim which the script will execute

## How to run
Install requirments (none so far)
```
pip3 install -r requirements.txt
```

### Attacker
Before running the script, the port can be changed if desired by directly changing the script
```
python3 server.py
```

### Victim
Before running the script, change the server ip to the attacker's ip by directly changing the script. The port can also be changed according
```
python3 victim.py
```
