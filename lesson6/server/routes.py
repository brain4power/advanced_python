from functools import reduce
from settings import INSTALLED_MODULES


def get_server_routes():
    return reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        reduce(
            lambda value, item: value + [getattr(item, 'routes', None)],
            reduce(
                lambda value, item: value + [__import__(f'{ item }.routes')],
                INSTALLED_MODULES,
                []
            ),
            []
        ),
        []
    )


def resolve(action, routes=None):
    routes_mapping = {
        route[0]['action']: route[0]['controller']
        for route in routes or get_server_routes()
    }
    return routes_mapping.get(action, None)
