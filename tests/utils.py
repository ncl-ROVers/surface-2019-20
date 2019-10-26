import inspect
import sys


def get_tests(module_name: str) -> dict:
    """
    TODO: Document

    :param module_name:
    :return:
    """

    def _is_test(obj):
        """
        TODO: Document

        :param obj:
        :return:
        """

        return inspect.isfunction(obj) and obj.__name__.startswith("test")

    # Declare the dictionary with tests - keys will be the function names and values will be the function objects
    tests = dict()

    # Fetch each test function in the module (sorted by source code order)
    for name, func in sorted(inspect.getmembers(sys.modules[module_name], predicate=_is_test),
                             key=lambda f: inspect.getsourcelines(f[1])[-1]):
        tests[name] = func

    return tests
