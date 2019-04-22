import json
import logging
from routes import resolve
from protocol import (
    validate_request, make_response,
    make_400, make_404
)
from settings import ENCODING_NAME


def handle_default_request(raw_request):
    request = json.loads(
        raw_request.decode(ENCODING_NAME)
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
                    logging.info(
                        f'Function { controller.__name__ } was called')
            except Exception as err:
                logging.critical(err, exc_info=True)
                response = make_response(
                    request, 500, 'Internal server error',

                )
        else:
            logging.error(f'Action { action_name } does not exits')
            response = make_404(request)
    else:
        logging.error(f'Request is not valid')
        response = make_400(request)

    return json.dumps(response).encode(ENCODING_NAME)
