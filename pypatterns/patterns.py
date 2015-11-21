from functools import wraps, partial
import re
from itertools import chain, repeat


class NoMatch(Exception):
    pass


class Any(object):
    def __init__(self, *allowed_types, _matcher=None, _repeat=False):
        self._allowed_types = allowed_types
        if _matcher is None:
            self.matcher = lambda arg: issubclass(type(arg),
                                                  tuple(self._allowed_types)) if self._allowed_types else True
        else:
            self.matcher = _matcher
        self._repeat = _repeat

    def __call__(self, arg):
        return self.matcher(arg)

    @staticmethod
    def of(*matches):
        baked_matches = _bake_predicates(matches)

        def of_matcher(arg):
            return any(map(lambda p: p(arg), baked_matches))

        return Any(_matcher=of_matcher)

    @staticmethod
    def has(*attrs, **attr_with_check):
        def has_matcher(arg):
            def has_attr_and_predicate(key_predicate):
                key, predicate = key_predicate
                return hasattr(arg, key) and _bake_predicate(predicate)(getattr(arg, key))

            return any(map(partial(hasattr, arg), attrs)) or any(
                map(has_attr_and_predicate, attr_with_check.items()))

        matcher = Any(_matcher=has_matcher)
        return matcher

    @staticmethod
    def re(str_or_re):
        pattern = re.compile(str_or_re)

        def re_matcher(arg):
            return bool(pattern.match(arg))

        return Any(_matcher=re_matcher)

    @staticmethod
    def args(*predicates):
        matcher = Any.of(*predicates)
        matcher._repeat = True
        return matcher


def _bake_predicate(p):
    if callable(p):
        return p
    else:
        return lambda a: a == p


def _bake_predicates(predicates):
    return [_bake_predicate(p) for p in predicates]


def _bake_kw_predicates(kw_predicates):
    return {k: p for k, p in kw_predicates if callable(p)}


def Pattern(*functions, wrap_fn=None):
    def wrapped(*args, **kwargs):
        for f in functions:
            try:
                return f(*args, **kwargs)
            except NoMatch:
                continue
        else:
            raise NoMatch
    if wrap_fn:
        wrapped = wraps(wrap_fn)(wrapped)
    return wrapped


def guard(*predicates, **kw_predicates):
    baked_predicates = _bake_predicates(predicates)
    baked_keyword_predicates = _bake_kw_predicates(kw_predicates)
    var_args_predicate = predicates[-1] if predicates and getattr(predicates[-1], '_repeat', False) else lambda a: False

    def test_args(args):
        return len(args) >= len(baked_predicates) and all(
            map(lambda p, x: p(x), chain(baked_predicates, repeat(var_args_predicate)), args))

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

        if fn.__name__ in fn.__globals__:
            old_definition = fn.__globals__[fn.__name__]
            # FIXME we're creating more recursion, no good in python
            return Pattern(decorated, old_definition)
        return decorated

    return decorator
