import json
import socket
import logging

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

handler = logging.FileHandler('main.log', encoding=encoding_name)
error_handler = logging.FileHandler('error.log', encoding=encoding_name)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        handler,
        error_handler,
        logging.StreamHandler(),
    ]
)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    logging.info(f'Server started with { host }:{ port }')
    client, address = sock.accept()
    logging.info(f'Client detected { address }')
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

                    if response.get('code') != 200:
                        logging.error(f'Request is not valid')
                    else:
                        logging.info(f'Function { controller.__name__ } was called')
                except Exception as err:
                    logging.critical(err, exec_info=True)
                    response = make_response(
                        request, 500, 'Internal server error'
                    )
            else:
                logging.error(f'Action { action_name } does not exits')
                response = make_404(request)
        else:
            logging.error(f'Request is not valid')
            response = make_400(request)
            
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding_name))
        client.send(s_response.encode(encoding_name))
        
except KeyboardInterrupt:
    logging.info('Client closed')
