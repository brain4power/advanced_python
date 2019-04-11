from .controller import (
    get_presence
)

routes = [
    {'action': 'presence', 'controller': get_presence}
]
