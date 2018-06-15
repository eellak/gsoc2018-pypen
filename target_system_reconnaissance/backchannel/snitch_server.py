import socket
import argparse


def receive(HOST ='192.168.1.215', PORT=1337):
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

    args = parser.parse_args()

    if not args.port:
        print('Define port')
        exit()

    receive(PORT=int(args.port))

    exit()
