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

You may also wish to compile the victim script to an exe with hidden execution (require pyinstaller)
The executable will be compiled in the 'dist' folder. It won't show any prompt when executed
```
pyinstaller --onefile --noconsole victim.py
```

## Custom commands
Custom commands are special commands that doesn't directly translate to the shell script to be executed by the victim
```
-> help
    - to see this page
-> exit 
    - to exit shell locally, victim return to trying to connect
-> exit_full 
    - to let victim exit too
-> simple
    - to simplify output
-> full
    - to use full output
-> file [file_name]
    - to get a file
-> screen 
    - take a screen shot and send it back
```
