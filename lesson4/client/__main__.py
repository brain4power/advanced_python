from datetime import datetime
import json
import socket
from yaml import load, Loader
from argparse import ArgumentParser

from routes import resolve
from protocol import (
    validate_request, make_response,
    make_400, make_404
)
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
    sock.connect((host, port))
    print(f'Client started with { host }:{ port }')
    while True:
        print('start loop')
        value = input('Enter data to send:')
        response = {
            'action': 'echo',
            'time': datetime.now().timestamp(),
            'data': value
        }
        s_response = json.dumps(response)
        b_response = s_response.encode(encoding_name)
        print('b_resp=', b_response)
        sock.send(b_response)
        print('sock sended')
        data = sock.recv(buffersize)
        print('data_recv=', data)
        print(data.decode(encoding_name))
except KeyboardInterrupt:
    print('Client closed')
