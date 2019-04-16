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

logger = logging.getLogger('main')
handler = logging.FileHandler('main.log', encoding=encoding_name)
error_handler = logging.FileHandler('error.log', encoding=encoding_name)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler.setLevel(logging.DEBUG)
error_handler.setLevel(logging.ERROR)
handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(error_handler)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    logger.info(f'Server started with { host }:{ port }')
    client, address = sock.accept()
    logger.info(f'Client detected { address }')
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
                        logger.error(f'Request is not valid')
                    else:
                        logger.info(f'Function { controller.__name__ } was called')
                except Exception as err:
                    logger.critical(err)
                    response = make_response(
                        request, 500, 'Internal server error'
                    )
            else:
                logger.error(f'Action { action_name } does not exits')
                response = make_404(request)
        else:
            logger.error(f'Request is not valid')
            response = make_400(request)
            
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding_name))
        client.send(s_response.encode(encoding_name))
        
except KeyboardInterrupt:
    logger.info('Client closed')
