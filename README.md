# PopcornShell
A simple python reverse shell project

## Introduction
The attacker host a server, await for the victim to execute the file

The victim file will constantly try to connect to the specified server.

Once a connection is established, the attacker can send commands to the victim which the script will execute

On Windows, the binary will copy itself to `C:\Users\{Username}\AppData\Roaming` and add that file to the registery `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` so it start with OS

## How to run
First, install requirments
```
pip3 install -r requirements.txt
```
Run the helper script
```
python3 run.py
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

## How to remove persistency on Windows
1. Remove the file `C:\Users\{Username}\AppData\Roaming\PopcornShell.exe`
2. Remove registery entry `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\PopcornShell`

## ScreenShots
[logo]: https://github.com/samsara138/PopcornShell/blob/main/Screenshots/ConnectedView.jpg "ConnectedView"
