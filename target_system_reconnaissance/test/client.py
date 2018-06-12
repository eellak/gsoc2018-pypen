import socket
import argparse


def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result


def main(HOST, PORT):
    s = socket.socket()
    s.connect((HOST, PORT))

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

    main(args.server, int(args.port))
