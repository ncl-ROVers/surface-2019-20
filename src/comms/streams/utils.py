import warnings as _warnings
from src.common import utils as _utils


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


def parse_sdp_content(content: str):
    content_data = {}

    body_lines = content.split("\r\n")
    i = 0

    # Parsing functions used in more than one place
    def __parse_option_i(line):
        __session_info = line[2:]

        if len(__session_info) <= 0:
            _warnings.warn(f"Session information field 'i' used but no information provided! " +
                           "This field will be skipped.", SyntaxWarning)
            return None

        return __session_info

    def __parse_option_c(line):
        __connection = line[2:].split(" ")

        if len(__connection) < 3:
            _warnings.warn(
                f"At least three values must be provided for the connection information field 'c', " +
                f"but only {len(__connection)} were found. This field will be skipped.", SyntaxWarning)
            return None

        return {"net_type": __connection[0], "addr_type": __connection[1], "address": __connection[2]}

    def __parse_option_b(line):
        __tokens = line[2:].split(":")

        if not len(__tokens) == 2:
            _warnings.warn(f"Bandwidth field 'b' must have two values, not {len(__tokens)}. " +
                           "This field will be skipped.", SyntaxWarning)
            return None

        if len(__tokens) > 0:
            return {"type": __tokens[0], "value": __tokens[1]}

        return None

    def __parse_option_k(line):
        __enc_tokens = line[2:].split(":")

        if len(__enc_tokens) == 1:
            return {"method": __enc_tokens[0]}
        elif len(__enc_tokens) == 2:
            return {"method": __enc_tokens[0], "key": __enc_tokens[1]}
        else:
            _warnings.warn(f"Encryption key field 'k' must have either one or two values. " +
                           "This field will be skipped.", SyntaxWarning)
            return None

    def __parse_option_a(line):
        __attrib_type_idx = _utils.index_of_safe(line, ':')
        if __attrib_type_idx == -1:
            return None

        __attribute = [ line[2:__attrib_type_idx], line[(__attrib_type_idx + 1):] ]

        if len(__attribute) == 1:
            if len(__attribute[0]) < 1:
                _warnings.warn("Attribute field cannot be of size less than one. " +
                               "This field will be skipped", SyntaxWarning)
                return None

            return __attribute[0], True
        elif len(__attribute) >= 2:
            if len(__attribute[0]) < 1 or len(__attribute[1]) < 1:
                _warnings.warn("Attribute field cannot be of size less than one. " +
                               "This field will be skipped", SyntaxWarning)
                return None

            return __attribute[0], __attribute[1]

        _warnings.warn("Empty attribute fields not allowed. This field will be skipped", SyntaxWarning)

        return None

    while i < len(body_lines):
        try:
            if len(body_lines[i]) < 1:
                continue

            if body_lines[i][0] == 'v':  # Parse version number
                version = int(body_lines[i][2:])
                if version != 0:
                    raise SyntaxError(f"Invalid protocol version number {version}.")
            elif body_lines[i][0] == 'o':  # Parse originator field
                tokens = body_lines[i][2:].split(' ')

                if not len(tokens) == 6:
                    raise SyntaxError(f"SDP originator field 'o' must have six fields. {len(tokens)} were provided!")

                content_data["originator"] = {}
                content_data["originator"]["name"] = tokens[0]
                content_data["originator"]["session"] = tokens[1]
                content_data["originator"]["username"] = tokens[2]
                content_data["originator"]["id"] = tokens[3]
                content_data["originator"]["version"] = tokens[4]
                content_data["originator"]["net_address"] = tokens[5]
            elif body_lines[i][0] == 's':  # Parse session name
                session_name = body_lines[i][2:]

                if len(session_name) < 1:
                    raise SyntaxError("Session name must be at least one character long!")

                content_data["name"] = session_name
            elif body_lines[i][0] == 'i':  # Parse session title/information
                session_info = __parse_option_i(body_lines[i])

                if session_info is None:
                    continue

                content_data["info"] = session_info
            elif body_lines[i][0] == 'u':  # Parse URI of description
                uri_desc = body_lines[i][2:]

                if len(uri_desc) <= 0:
                    _warnings.warn(f"Description URI field 'u' used but no URI provided! " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                content_data["uri_desc"] = uri_desc
            elif body_lines[i][0] == 'e':  # Parse contact emails
                emails = body_lines[i][2:]

                if len(emails) > 0:
                    content_data["emails"] = emails.split(" ")
                else:
                    content_data["emails"] = []
            elif body_lines[i][0] == 'p':  # Parse contact phone numbers
                phones = body_lines[i][2:]

                if len(phones) > 0:
                    content_data["phones"] = phones.split(" ")
                else:
                    content_data["phones"] = []
            elif body_lines[i][0] == 'c':  # Parse connection information
                connection = __parse_option_c(body_lines[i])

                if connection is None:
                    continue

                content_data["connection_info"] = connection
            elif body_lines[i][0] == 'b':  # Parse bandwidth information
                bandwidth_info = __parse_option_b(body_lines[i])

                if bandwidth_info is None:
                    continue

                bw_list = content_data.get("bandwidths", [])
                bw_list.append(bandwidth_info)
                content_data["bandwidths"] = bw_list
            elif body_lines[i][0] == 't':  # Parse timing description
                time_tokens = body_lines[i][2:].split(" ")

                if not len(time_tokens) == 2:
                    _warnings.warn(f"Timing field 't' must have two values, not {len(time_tokens)}. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                time_desc = {
                    "start_time": time_tokens[0],
                    "end_time": time_tokens[1],
                    "repeat_times": []
                }

                while (len(body_lines) > (i + 1)) and (len(body_lines[i + 1]) > 0) and (body_lines[i + 1][0] == 'r'):
                    repeat_tokens = body_lines[i + 1][2:].split(" ")

                    if not len(repeat_tokens) == 3:
                        _warnings.warn(f"Repeat timing field 'r' must have three values, not {len(repeat_tokens)}. " +
                                       "This field will be skipped.", SyntaxWarning)
                        continue

                    time_desc["repeat_times"].append({
                        "interval": repeat_tokens[0],
                        "duration": repeat_tokens[1],
                        "offset": repeat_tokens[2]
                    })

                    i += 1

                times = content_data.get("time_descriptions", [])
                times.append(time_desc)

                content_data["time_descriptions"] = times
            elif body_lines[i][0] == 'r':  # Parse repeat timing line
                _warnings.warn(f"Repeat time field 'r' detected outside of time description. " +
                               "This field will be skipped.", SyntaxWarning)
            elif body_lines[i][0] == 'z':  # Parse time zone info
                zone_tokens = body_lines[i][2:].split(" ")

                if (len(zone_tokens) < 2) or (len(zone_tokens) % 2 == 1):
                    _warnings.warn(f"Time zone field 'r' must have an even, positive number of values. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                content_data["zones"] = [(zone_tokens[i], zone_tokens[i + 1]) for i in range(0, len(zone_tokens), 2)]
            elif body_lines[i][0] == 'k':
                enc_tokens = __parse_option_k(body_lines[i])

                if enc_tokens is None:
                    continue

                content_data["encryption"] = enc_tokens
            elif body_lines[i][0] == "m":  # Parse media description
                media_tokens = body_lines[i][2:].split(" ")

                if media_tokens[1].find("/") == -1:
                    start_port = int(media_tokens[1])
                    port_count = 1
                else:
                    start_port = int(media_tokens[1][:media_tokens[1].find("/")])
                    port_count = int(media_tokens[1][(media_tokens[1].find("/") + 1):])

                media = {
                    "media": {
                        "type": media_tokens[0],
                        "start_port": start_port,
                        "port_count": port_count,
                        "protocol": media_tokens[2],
                        "formats": media_tokens[3:]
                    }
                }

                while (len(body_lines) > (i + 1)) and not \
                        ((len(body_lines[i + 1]) == 0) or (body_lines[i + 1][0] == 'm')):
                    i += 1

                    if body_lines[i][0] == 'i':
                        session_info = __parse_option_i(body_lines[i])
                        if session_info is None:
                            continue

                        media["info"] = session_info
                    elif body_lines[i][0] == 'c':
                        connection = __parse_option_c(body_lines[i])
                        if connection is None:
                            continue

                        media["connection_info"] = connection
                    elif body_lines[i][0] == 'b':
                        bandwidth_info = __parse_option_b(body_lines[i])

                        if bandwidth_info is None:
                            continue

                        bw_list = media.get("bandwidths", [])
                        bw_list.append(bandwidth_info)
                        media["bandwidths"] = bw_list
                    elif body_lines[i][0] == 'k':
                        enc_tokens = __parse_option_k(body_lines[i])

                        if enc_tokens is None:
                            continue

                        media["encryption"] = enc_tokens
                    elif body_lines[i][0] == 'a':
                        attribute = __parse_option_a(body_lines[i])

                        if attribute is None:
                            continue

                        attr_list = media.get("attributes", [])
                        attr_list.append(attribute)
                        media["attributes"] = attr_list

                media_desc = content_data.get("media_descriptions", [])
                media_desc.append(media)
                content_data["media_descriptions"] = media_desc
            elif body_lines[i][0] == 'a':
                attribute = __parse_option_a(body_lines[i])

                if attribute is None:
                    continue

                attr_list = content_data.get("attributes", [])
                attr_list.append(attribute)
                content_data["attributes"] = attr_list
        finally:
            i += 1

    return content_data