import socket
import argparse
import os

import full_scan


def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result


def retrieve(HOST, PORT):
    s = socket.socket()
    s.connect((HOST, PORT))

    for root, dirs, files in os.walk('/results'):
        for file in files:
            with open(os.path.join(root, file), "rb") as send_file:
                s.sendall(file)
                s.sendall(send_file)

    while True:
        data = bytes_to_int(s.recv(1024))
        data += 1
        s.sendall(bytes([data]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # server address
    parser.add_argument('-server', help='Server address')
    # port
    parser.add_argument('-port', help='Port')

    args = parser.parse_args()

    full_scan

    retrieve(args.server, int(args.port))
