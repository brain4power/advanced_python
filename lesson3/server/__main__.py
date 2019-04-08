import socket
from yaml import load, Loader
from argparse import ArgumentParser

from settings import (
    ENCODING_NAME, HOST,
    PORT, BUFFERSIZE
)

host = HOST
port = PORT
encoding_name = ENCODING_NAME
buffersize = BUFFERSIZE

parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        config = load(file, Loader=Loader)
        host = config.get('host') or HOST
        port = config.get('port') or PORT
        encoding_name = config.get('encoding_name') or ENCODING_NAME
        buffersize = config.get('buffersize') or BUFFERSIZE

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    print(f'Server started with {host}:{port}')
    while True:
        client, address = sock.accept()
        print(f'Client detected {address}')
        data = client.recv(buffersize)
        print(data.decode(encoding_name))
        client.send(data)
except KeyboardInterrupt:
    print('Server closed')
