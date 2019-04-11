import json
import socket
from yaml import load, Loader
from argparse import ArgumentParser

import settings

from routes import resolve
from protocol import (
    validate_request, make_response,
    make_400, make_404
)
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
    print(f'Server started with { host }:{ port }')
    client, address = sock.accept()
    print(f'Client detected { address }')
    while True:
        b_request = client.recv(buffersize)
        en_data = b_request.decode(encoding_name)
        req = json.loads(en_data)
        request = json.loads(
            b_request.decode(encoding_name)
        )
        action_name = request.get('action')

        if validate_request(request):
            controller = resolve(action_name)
            if controller:
                try:
                    response = controller(request)
                except Exception as err:
                    print('err=', err)
                    response = make_response(
                        request, 500, 'Internal server error'
                    )
            else:
                print('Action { action_name } does not exits')
                response = make_404(request)
        else:
            print('Request is not valid')
            response = make_400(request)
            
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding_name))
        print('server send:', s_response.encode(encoding_name))
        
except KeyboardInterrupt:
    print('Client closed')
