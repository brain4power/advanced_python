import socket
from yaml import load, Loader
from argparse import ArgumentParser

from settings import (
    ENCODING_NAME, VARIABLE, HOST,
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
    sock.connect((HOST, PORT))
    print(f'Client started with { HOST }:{ PORT }')
    while True:
        value = input('Enter data to send:')
        bvalue = value.encode(ENCODING_NAME)
        sock.send(bvalue)
        data = sock.recv(BUFFERSIZE)
        print(data.decode(ENCODING_NAME))
except KeyboardInterrupt:
    print('Client closed')
