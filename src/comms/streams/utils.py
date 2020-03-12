def http_find_option(lines, option_name) -> str:
    """
    Find the value of an option inside an HTTP header.

    :param lines: A list of all the lines of the HTTP header.
    :param option_name: The name of the option to search for.
    :return: The value of the option.
    """
    option = list(filter(lambda line: line.lower().startswith(option_name.lower()), lines))

    if len(option) > 0:
        return option[-1][(option[-1].find(":") + 1):]

    return ""
