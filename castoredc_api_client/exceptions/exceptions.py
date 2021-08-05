import functools


class NotFoundException(Exception):
    pass


class CastorException(Exception):
    pass


def castor_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arguments = list(args)
        client = arguments[0]
        try:
            return func(*args, **kwargs)
        except CastorException as e:
            raise

    return wrapper
