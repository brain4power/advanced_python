from .controllers import (
    get_exception
)

routes = [
    {'action': 'error', 'controller': get_exception}
]
