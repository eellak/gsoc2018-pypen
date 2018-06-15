import socket
import argparse
import os
import sys
sys.path.append('../')

import full_scan


def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result


def retrieve(HOST, PORT):
    for root, dirs, files in os.walk('results_info'):
        for file in files:
            s = socket.socket()
            s.connect((HOST, PORT))
            f_read = None
            with open(os.path.join(root, file), "rb") as send_file:
                s.send(bytearray(file, encoding='utf-8'))
                f_read = send_file.read(1024)

                while len(f_read):
                    s.send(f_read)
                    f_read = send_file.read(1024)
                s.close()

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytearray('DONE', encoding='utf-8'))
    s.close()

    return None




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # server address
    parser.add_argument('-server', help='Server address')
    # port
    parser.add_argument('-port', help='Port')

    args = parser.parse_args()

    full_scan.main()

    retrieve(args.server, int(args.port))
