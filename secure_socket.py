import socket
import sys
import time


def print_bytes(data):
    for i in data:
        print(hex(i), end=" ")
    print("\n\n")


# A general purpose secure socket that ensure full data sending and reciving
class SecureSocket:
    sock = None
    destination_address = ""

    # For server
    connection = None
    payload_size = 1024

    def __init__(self, payload_size=100):
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
                print(f"Trying to connect to server at {self.destination_address}...")
                time.sleep(1)

    # Server waiting for a connection
    def wait_for_connection(self, ip="0.0.0.0", port=7123):
        self.destination_address = (ip, port)
        # Bind the socket to accept any ip at port
        self.sock.bind(self.destination_address)
        print(f"Waiting for connection on {self.destination_address} ...")
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

        data_packet = f'{len(segments)} {self.payload_size}'.encode()
        data_packet += bytes.fromhex("00") * (self.payload_size - len(data_packet))
        print("Data packet =>",data_packet)
        segments.insert(0, data_packet)

        active_connection = self.connection if self.connection else self.sock
        for segment in segments:
            try:
                active_connection.send(segment)
            except:
                print("Connection broken")
                self.close()
                return False
        return True

    # receive a payload, optional to have a post process function
    def receive(self, post_process=None):
        payload = bytes()
        active_socket = self.connection if self.connection else self.sock

        while True:
            info_packet = active_socket.recv(self.payload_size)
            info_packet = info_packet.rstrip(b'\x00').decode().split(" ")
            segment_count = int(info_packet[0])
            sender_payload_size = int(info_packet[1])

            for i in range(segment_count):
                segment = active_socket.recv(sender_payload_size)
                if len(segment) == 0:
                    return bytes()
                payload += segment
            if post_process:
                payload = post_process(payload)
            return payload

    def close(self):
        self.sock.close()
        if self.connection:
            self.connection.close()


# Example code for setting up a server
def setup_server():
    secure_socket = SecureSocket()
    secure_socket.wait_for_connection()
    secure_socket.send("Hello world")
    payload = secure_socket.receive()


# Example code for setting up a client
def setup_client():
    secure_socket = SecureSocket()
    secure_socket.connect()
    data = secure_socket.receive()
    secure_socket.send("Hello to you too")
