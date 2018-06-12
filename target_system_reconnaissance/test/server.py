import socket
import argparse
import time


def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result


def main(HOST = '192.168.1.215', PORT=1337):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print('Server listening on port {}...'.format(PORT))

    conn, _ = s.accept()

    data = 0

    while True:
        data += 1
        conn.send(bytes([data]))
        data = bytes_to_int(conn.recv(4096))
        time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # port
    parser.add_argument('-port', help='Port')

    args = parser.parse_args()

    if not args.port:
        print('Define port')
        exit()

    main(PORT=int(args.port))
