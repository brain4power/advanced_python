import logging


logger = logging.getLogger('decorators')


def logged(func):
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{ func.__name__ } - { request }, args= {args}')
        return func(request, *args, **kwargs)
    
    return wrapper
