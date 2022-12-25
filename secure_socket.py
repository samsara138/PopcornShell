import socket
import sys
import time
import PKCS7

# A general purpose secure socket that ensure full data sending and reciving
class SecureSocket:
    sock = None
    destination_address = ""

    # For server
    connection = None
    payload_size = 300

    def __init__(self, payload_size = 1024):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.payload_size = payload_size

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
        if len(payload) == 0:
            print("Error: Empty payload", file=sys.stderr)
            return False

        segments = []
        while len(payload) > 0:
            segments.append(payload[:self.payload_size])
            payload = payload[self.payload_size:]
        if len(segments[-1]) == self.payload_size:
            empty_payload = PKCS7.pad(bytes(), self.payload_size)
            segments.append(empty_payload)
        else:
            segments[-1] = PKCS7.pad(segments[-1], self.payload_size)

        active_connection = self.connection if self.connection else self.sock
        for segment in segments:
            active_connection.send(segment)

    # receive a payload, optional to have a post process function
    def receive(self, post_process=None):
        payload = bytes()
        active_socket = self.connection if self.connection else self.sock

        while True:
            buffer = active_socket.recv(1024)
            if PKCS7.is_padded(buffer)[0]:
                payload += PKCS7.remove_padding(buffer)
                break
            payload += buffer

        if post_process:
            payload = post_process(payload)
        return payload
