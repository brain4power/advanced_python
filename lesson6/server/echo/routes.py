from .controller import (
    get_echo
)

routes = [
    {'action': 'echo', 'controller': get_echo}
]
