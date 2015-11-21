from lib2to3.patcomp import PatternSyntaxError

import pytest

from pypatterns.patterns import guard, Any, NoMatch, Pattern


def test_explicitly_combined_patterns():
    @guard(Any.of(0, 1))
    def fib0(n):
        return 1

    @guard(Any(int))
    def fib(n):
        return fib(n - 1) + fib(n - 2)

    fib = Pattern(fib0, fib)
    assert fib(0) == 1
    assert fib(1) == 1
    assert fib(2) == 2
    assert fib(3) == 3
    with pytest.raises(NoMatch):
        fib('not a number')


@guard(Any(int), Any(int))
def top_scope(a, b):
    return a + b


@guard(Any(int))
def top_scope(a):
    return a * 2


def test_combining_module_scope_patterns():
    assert top_scope(2, 3) == 5
    assert top_scope(2) == 4
    with pytest.raises(NoMatch):
        top_scope('1', '2')
    with pytest.raises(NoMatch):
        top_scope()


def test_combining_methods():
    class A():
        @guard(Any(str), Any(str))
        def m(self, s1, s2):
            return s1 + s2

        @guard(Any(int), Any(int))
        def m(self, i1, i2):
            return i1 ** i2

    a = A()
    assert a.m('hello', ' world') == 'hello world'
    assert a.m(2, 3) == 2 ** 3
    with pytest.raises(NoMatch):
        a.m(2, '3')
    with pytest.raises(NoMatch):
        a.m('2', 3)
    with pytest.raises(NoMatch):
        a.m('2')
