import socket
import sys
import time

# A secure socket that ensure full data sending and reciving
class SecureSocket:
    sock = None
    destination_address = ""

    # For server
    connection = None

    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Client connect to a server
    def connect(self, ip="localhost", port=7123):
        # Connect the socket to the server
        self.destination_address = (ip, port)
        # Keep trying to connect to the server
        while True:
            try:
                self.sock.connect(self.destination_address)
                print("Connected!")
                break
            except:
                print("Trying to connect to server ...")
                time.sleep(1)

    # Server waiting for a connection
    def wait_for_connection(self, ip="0.0.0.0", port=7123):
        server_address = (ip, port)
        # Bind the socket to accept any ip at port
        self.sock.bind(server_address)
        print("Waiting for connection ...")
        self.sock.listen()
        # Accept an incoming connection
        self.connection, self.destination_address = self.sock.accept()
        print('Connected by', self.destination_address)

    # Send a payload
    def send(self, payload):
        if self.connection:
            self.connection.send(payload)
        else:
            self.sock.send(payload)

    # receive a payload
    def receive(self):
        if self.connection:
            payload = self.connection.recv(1024)
        else:
            payload = self.sock.recv(1024)
        return payload
