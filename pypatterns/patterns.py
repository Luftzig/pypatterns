from functools import wraps


class NoMatch(Exception):
    pass


class Any(object):

    def __init__(self, *types):
        pass


def guard(*predicates, **kw_predicates):
    def decorator(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            return fn()
        return decorated
    return decorator
