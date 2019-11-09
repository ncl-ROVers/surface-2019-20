
"""
main.py
====================================
The core module of my example project
"""

def about_me(your_name: str) -> str:
    """
    Return the most important thing about a person.

    Parameters
    ----------
    your_name
        A string indicating the name of the person.

    :func:`ExampleClass.about_self` is very nice
    :py:mod:`another` is also very nice

    :param your_name: Name to put in
    :return: String
    """

    x = 0
    return "The wise {} loves Python.".format(your_name)


class ExampleClass:
    """An example docstring for a class definition."""

    def __init__(self, name):
        """
        Blah blah blah.
        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        """
        self.name = name

    def about_self(self):
        """
        Return information about an instance created from ExampleClass.
        """
        return "I am a very smart {} object.".format(self.name)

class SimpleClass:
    """This is an example of class documentation"""

    def printHello():
        print('Hi!')