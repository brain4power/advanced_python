from datetime import datetime
from ..controller import get_presence
from ...protocol import make_400


def test_get_presence():
    request = {
        "action": "presence",
        "time": datetime.now().timestamp(),
        "type": "status",
        "user": {
            "account_name": "C0deMaver1ck"
        }
    }

    response = get_presence(request)

    assert response == make_400(request)
