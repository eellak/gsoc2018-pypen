import socket
import argparse


def receive(HOST = '192.168.1.215', PORT=1337):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print('Server listening on port {}...'.format(PORT))

    conn, _ = s.accept()

    while True:
        in_data = conn.recv(1024)
        if 'EOF' in str(in_data.decode('utf-8')):
            in_data = bytearray(str(in_data.decode('utf-8')).rsplit('EOF')[1], encoding='utf-8')
        if str(in_data.decode('utf-8')).endswith('.json'):
            out_file = open(str(in_data.decode('utf-8')), 'wb')

        while in_data:
            out_file.write(in_data)
            in_data = conn.recv(1024)
            out_file.write(in_data)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # port
    parser.add_argument('-port', help='Port')

    args = parser.parse_args()

    if not args.port:
        print('Define port')
        exit()

    receive(PORT=int(args.port))
