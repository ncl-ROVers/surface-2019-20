# Testing infrastructure

## Unit tests

We are using [pytest](https://docs.pytest.org/en/latest/contents.html) as our unit testing infrastructure. The test
files and the test functions must match the following patterns: `test_*` or `*_test`.

#### Running the tests

You can run the tests using either the command prompt as described
[here](https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest), or in *PyCharm* by
selecting the `tests` folder and selecting *Run 'pytest in tests'*. More information is available
[here](https://www.jetbrains.com/help/pycharm/pytest.html#run-pytest-test).

The results will be displayed in the *Run* window.

#### Examples

Here is an example test function from `log_test.py`:

```python
def test_create_logs():

    Log.debug("Test debug message")
    Log.info("Test info message")
    Log.warning("Test warning message")
    Log.error("Test error message")

    # There should be 5 files created - each for the log level and a verbose file for all levels combined
    assert len(get_log_files()) == 5
```

Notice that both the module and the function contain the `_test` (or `test_`) expression in their names.
