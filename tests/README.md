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

Here is an example of a configuration function which runs before all tests are executed:

```python
@pytest.fixture(scope="module", autouse=True)
def config():
    """
    PyTest fixture for the configuration function - used to execute config before any test is ran.

    `scope` parameter is used to share fixture instance across the module session, whereas `autouse` ensures all tests
    in session use the fixture automatically.
    """

    # Remove all log files from the assets folder.
    for log_file in get_log_files():
        os.remove(log_file)

    # Reconfigure the logger to use a separate folder (instead of the real logs)
    Log.reconfigure(Logger.MAIN, os.path.join(COMMON_LOGGER_DIR, "config_main.json"),
                    log_directory=TESTS_ASSETS_DIR)
```

You can use a similar structure in your code to configure your environment before running the tests.
