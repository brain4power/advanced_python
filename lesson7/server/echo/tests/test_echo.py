from datetime import datetime
from echo.controller import get_echo


def test_get_echo():
    data = 'Some data'

    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': data
    }

    response = get_echo(request)

    assert response.get('data') == data
