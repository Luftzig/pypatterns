# PyPatterns
Functional-style Pattern Matching for Python

## Overview

This library is intended to provide facility in Python to bind together
several callables to a single callable object that will dispatch the correct
function by predetermined rules.

For example:

    @guard(Any.of(0, 1))
    def fibonacci(n):
        return 1

    @guard(Any(int))
    def fibonacci(n):
        return fibonacci(n - 1) + fibonacci(n - 2)


    >>> fibonacci(3)
    3

## Use &amp; Concepts

### `guard` decorator
Turns any method of function into a guarded one.
The function decorated by `guard` will only be invoked if it's arguments
match the rules provided to `guard`.

If several functions in same scope use the same name and have been decorated
by `guard`, the resulting function will check all previously decorated
functions (including the current one) for a match.

### Rules matching

As a general rule, `guard` will match positional arguments to positional arguments
and keyword arguments to keyword arguments. Exceptional rules can be made
to match `*args` and `**kwards`.

#### Literals
`guard(1, "Hello", 3.1415, True)` will match if invoked with the arguments `1, "Hello", 3.1415, True`.
Literal matching will try to match any object that is not of type `type` or is not
callable so take caution when using objects that are comparable only by their
`id(x)` result.

#### Tests
`guard` can use callables that will be invoked on the argument to determine
if it can be passed to the function. The test function must accept one argument
and return True if argument can be passed to the decorated function or False otherwise.

#### The `Any` Object
The special object `Any`, when used as an argument to `guard` will match any
value. `Any(t)` for type `t` will match any object which is is an instance or
subclass of type `t`.

##### `Any.of(*values)`
Meant for use in literals, where any of the literals given as arguments to `Any.of`
is a valid match.

##### `Any.has(*attributes, **attributesWithMatch)`
`Any.has("attr1", "attr2")` will only match objects `o` for which `hasattr(o, "attr1")`
and `hasattr(o, "attr2")` is true.
`Any.has(attr1=int, attr2=3)` will only match objects `o` for which there exists
attributes "attr1" and "attr2" and the attached rules apply recursively, that is:
`o.attr1` is of type `int` and `o.attr2 == 2`

##### `Any.re(<str or regex>)`

Will match any string that matches the supplied regular expression object
or the regular expression compiled from string.

#### Variable arguments and variable keyword arguments
`Any.args(*rules)`, when given as the last positional argument will match
any extra positional arguments according to the provided rules. Arguments
must match at least one rule to be valid.
`Any.kwargs(key_rule, *value_rules)` will match any extra keyword arguments
if the can match `key_rule` and at least one of `value_rules`.

#### Collections
**TBD**
We would like to provide rules for matching collections recursively such
as mapping and iterable types.

## Long term goals

Other possibles goals for this project are:
* Support object, mapping and iterable the construction.
* Export to other programming languages (such as Javascript)


