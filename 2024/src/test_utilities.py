import re
from collections.abc import Callable, Sequence
from copy import deepcopy
from typing import Any

from termcolor import colored

TestDict = dict[str, Any]
AssertFunction = Callable[[Any, Any], bool]


def test(*args, **kwargs) -> Callable[[Callable[..., Any]], None]:
    """
    Decorator to run parameterized tests using run_tests_params.

    keyword argument:
        tests: Sequence[Sequence[Any]] = [{
            "name": "test",
            "diagram": "###A###",
            "expected": "A"}
        ],
        assert_funct: AssertFunction = lambda x, y: x == y

    Returns:
        A decorator that runs the tests.

    Example:
        >>> @test(tests=[{"name": "test", "diagram": "###A###", "expected": "A"}])
        ... def dummy(diagram):
        ...     return diagram[3]
        test test passed, for dummy.
        Success
    """

    def decorator(func: Callable[..., Any]) -> None:
        run_tests_params(func, *args, **kwargs)

    return decorator


def run_tests(
    f: Callable[..., Any],
    tests: Sequence[Sequence[Any]],
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> None:
    """
    Run a series of tests on a function.

    Args:
        f: Function to test.
        tests: Sequence of test cases, each a sequence where the last element is expected output.
        assert_funct: Function to compare actual and expected output.

    Example:
        >>> def add(a, b): return a + b
        >>> run_tests(add, [["sum", 2, 3, 5], ["zero", 0, 0, 0]])
        test sum passed, for add.
        test zero passed, for add.

        Success
    """

    def test(*args: Any) -> None:
        expected = args[-1]
        actual = f(*args[:-1])
        if not assert_funct(actual, expected):
            raise AssertionError(f"{actual} should be {expected}")

    no_errors = True
    for _args in deepcopy(tests):
        name = ""
        try:
            name, *_args = _args
            test(*_args)
            print(colored(f"test {name} passed, for {f.__name__}.", "green"))
        except Exception as e:
            print(
                colored(f"test {name} failed! ***{e.args}, for {f.__name__}.", "red")
            )  # noqa
            no_errors = False

    print()
    if no_errors:
        print(colored("Success", "green"))
    else:
        print(colored("***Errors", "red"))


def test_all_solutions(
    test_harnass, obj, pattern, tests, assert_funct=lambda x, y: x == y
) -> None:
    found = False
    for method in (e for e in dir(obj) if re.match(pattern, e)):
        run_tests(test_harnass(getattr(obj(), method)), tests, assert_funct)
        found = True
        print("\n" * 2)

    if found:
        print(colored("All matched methodes have been tested.", "green"))
    else:
        print(
            colored(
                "***There was no method, that did match the pattern!", "red"
            )  # noqa
        )  # noqa


def run_tests_params(f, tests, assert_funct=lambda x, y: x == y):
    def _test(test) -> bool:
        name, *params, expected = test.items()
        _, name = name
        _, expected = expected
        params = dict(params)
        actual = f(**params)
        if assert_funct(actual, expected):
            print(colored(f"Test {name} passed, for {f.__name__}.", "green"))
            return True
        print(
            colored(
                f"Test {name }: {actual} should be {expected}, for {f.__name__}.",  # noqa
                "red",
            )
        )
        return False

    print()
    all_passed = True
    for test in deepcopy(tests):
        all_passed &= _test(test)

    if all_passed:
        print(colored("Success", "green"))
    else:
        print(colored("***Errors", "red"))


def test_all_solutions_params(
    test_harnass,
    obj,
    tests,
    pattern=r"^[^_+]",
    assert_funct=lambda x, y: x == y,
) -> None:
    found = False
    for method_name in (e for e in dir(obj()) if re.match(pattern, e)):
        method = getattr(obj(), method_name)

        run_tests_params(test_harnass(method), tests, assert_funct)
        found = True
        print("\n" * 2)

    if found:
        print(colored("All matched methodes have been tested.", "blue"))
    else:
        print(colored("***There was no method, that did match the pattern!", "red"))


def standard_test_harnass(f) -> Callable[..., Any]:
    def func(**kwarg):
        actual = f(**kwarg)
        return actual

    func.__name__ = f.__name__
    return func
