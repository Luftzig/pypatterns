import pytest
from pypatterns.patterns import guard, NoMatch, Any


@pytest.fixture
def zero_arg_fn():
    def zero_args():
        return 'Test'
    return zero_args


def test_return_decorator(zero_arg_fn):
    result = guard()(zero_arg_fn)
    assert callable(result)
    invoke_result = result()
    assert invoke_result == 'Test'


@pytest.fixture
def one_arg_fn():
    def one_arg(x):
        return x + 1
    return one_arg


def test_run_function_if_predicate_function(one_arg_fn):
    fn = guard(lambda x: x == 2)(one_arg_fn)
    with pytest.raises(NoMatch):
        fn(3)
    assert fn(2) == 3


def test_any_argument(one_arg_fn):
    fn = guard(Any)(one_arg_fn)
    assert fn(3) == 4
    assert fn(2) == 3


def test_literal_string_predicate():
    def fn(a):
        return a + ' string'
    g = guard('this is a')(fn)
    with pytest.raises(NoMatch):
        g(0)
    with pytest.raises(NoMatch):
        g('')
    assert g('this is a') == 'this is a string'


def test_literal_integer_predicate():
    def f(x):
        return 2 * x
    g = guard(4)(f)
    with pytest.raises(NoMatch):
        g('Something')
    with pytest.raises(NoMatch):
        g(3)
    assert g(4) == 8


def test_literal_object_predicate():
    o = object()

    def f(x):
        return True
    g = guard(o)(f)
    with pytest.raises(NoMatch):
        g(0)
    with pytest.raises(NoMatch):
        g(object)
    assert g(o)


def test_type_predicate():
    def f(a, b):
        return a * b
    g = guard(Any(str), Any(int))(f)
    with pytest.raises(NoMatch):
        g('eee', 'k')
    with pytest.raises(NoMatch):
        g(3, 2)
    with pytest.raises(NoMatch):
        g('eeeeeeeeee', None)
    assert g('eeky', 3) == 'eekyeekyeeky'


def test_literal_type_is_treated_as_object():
    def f(obj, int_type):
        return int_type(obj)
    g = guard(Any, int)(f)
    with pytest.raises(NoMatch):
        g('1234', float)
    assert g('1234', int) == 1234


def test_has_attribute_predicate():
    def f(x):
        return x.count(2)
    g = guard(Any.has('count'))(f)
    with pytest.raises(NoMatch):
        g({})
    with pytest.raises(NoMatch):
        g(1)
    assert g((1, 2, 2, 3)) == 2


def test_has_with_predicate():
    X = type('X', (object, ), {'value': None})

    def f(x):
        return x.value
    g = guard(Any.has(value=Any(int)))(f)
    with pytest.raises(NoMatch):
        g('123')
    with pytest.raises(NoMatch):
        x = X()
        x.value = '321'
        g(x)
    x = X()
    x.value = 321
    assert g(x) == 321


def test_with_regex_matching():
    def f(s):
        return s
    g = guard(Any.re('A|B'))(f)
    with pytest.raises(NoMatch):
        g('Cat')
    with pytest.raises(NoMatch):
        g('CAT')
    assert g('About') == 'About'


@pytest.mark.skipif(True, reason="TBD")
def test_any_of_legal_values():
    assert 0


@pytest.mark.skipif(True, reason="TBD")
def test_with_keyword_args():
    assert 0


def test_check_varargs():
    def count_args(*args):
        return len(args)
    g = guard(1, Any.args(Any(int)))(count_args)
    with pytest.raises(NoMatch):
        g(0)
    with pytest.raises(NoMatch):
        g(1, 'a')
    with pytest.raises(NoMatch):
        g(1, *(['a'] * 20))
    assert g(1, 2, 3) == 3
    assert g(*([1] * 20)) == 20


@pytest.mark.skipif(True, reason="TBD")
def test_check_variable_keyword_args():
    assert 0


def test_any_with_no_types():
    def f(x):
        return x
    g = guard(Any())(f)
    assert g(3) == 3


def test_none_as_literal():
    def f(x):
        return x is None
    g = guard(None)(f)
    with pytest.raises(NoMatch):
        g(True)
    assert g(None)


@pytest.mark.skipif(True, reason="TBD")
def test_any_with_none_object():
    assert 0

