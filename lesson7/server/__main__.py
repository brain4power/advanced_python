import json
import socket
import select
import logging

from yaml import load, Loader
from argparse import ArgumentParser

from handlers import handle_default_request
import settings

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

requests = []
connections = []

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.settimeout(0)
    sock.listen(5)
    logging.info(f'Server started with { host }:{ port }')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client detected { address }')
            connections.append(client)
        except Exception:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for w_client in rlist:
            b_request = w_client.recv(buffersize)
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for r_client in wlist:
                r_client.send(b_response)
        
except KeyboardInterrupt:
    logging.info('Client closed')
