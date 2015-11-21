from functools import wraps, partial
import re


class NoMatch(Exception):
    pass


class Any(object):

    def __init__(self, *allowed_types):
        self._allowed_types = allowed_types

    def __call__(self, arg):
        if hasattr(self, 'matcher'):
            return self.matcher(arg)
        return issubclass(type(arg), tuple(self._allowed_types))

    @staticmethod
    def of(*matches):
        pass

    @staticmethod
    def has(*attrs, **attr_with_check):
        matcher = Any()

        def has_matcher(arg):
            def has_attr_and_predicate(key_predicate):
                key, predicate = key_predicate
                return hasattr(arg, key) and _bake_predicate(predicate)(getattr(arg, key))

            return any(map(partial(hasattr, arg), attrs)) or any(
                map(has_attr_and_predicate, attr_with_check.items()))

        matcher.matcher = has_matcher
        return matcher

    @staticmethod
    def re(str_or_re):
        pass


def _bake_predicate(p):
    if callable(p):
        return p
    elif isinstance(p, Any):
        return p
    else:
        return lambda a: a == p


def _bake_predicates(predicates):
    return [_bake_predicate(p) for p in predicates]


def _bake_kw_predicates(kw_predicates):
    return {k: p for k, p in kw_predicates if callable(p)}


def guard(*predicates, **kw_predicates):
    baked_predicates = _bake_predicates(predicates)
    baked_keyword_predicates = _bake_kw_predicates(kw_predicates)

    def test_args(args):
        # TODO no length matching
        return all(map(lambda p, x: p(x), baked_predicates, args))

    def test_kw_args(kwargs):
        # TODO no length matching
        return all(map(lambda p_item: p_item[1](kwargs[p_item[0]]), baked_keyword_predicates))

    def decorator(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if test_args(args) and test_kw_args(kwargs):
                return fn(*args, **kwargs)
            else:
                raise NoMatch
        return decorated
    return decorator
