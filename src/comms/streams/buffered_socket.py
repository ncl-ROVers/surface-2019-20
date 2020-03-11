import socket as _socket


class BufferedSocket(_socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__stream_buffer = bytearray()

    def __read_ahead(self):
        """
        Read bytes from the socket into the stream buffer.
        """
        data = self.recv(4096)
        self.__stream_buffer.extend(data)

    def __collapse_head(self, head_size):
        """
        Remove the section [0, head_size) from the start of the buffer.
        The remaining data will be moved to the beginning of the buffer.

        :param head_size: The amount of bytes to remove from the start of the buffer.
        """
        self.__stream_buffer = self.__stream_buffer[head_size:]

    def read_until(self, delim):
        """
        Read from the strean until 'delim' is encountered.

        :param delim: The sequence of bytes that terminates reading.
        """
        delim_index = 0

        while True:
            if delim_index >= len(self.__stream_buffer):
                self.__read_ahead()

            if self.__stream_buffer[delim_index:(delim_index + len(delim))] == bytearray(delim):
                break

            delim_index += 1

        data = self.__stream_buffer[:delim_index]
        self.__collapse_head(delim_index + len(delim))

        return data

    def read_amount(self, count):
        """
        Read a number of bytes from the stream.

        :param count: The number of bytes to be read.
        """
        while len(self.__stream_buffer) < count:
            self.__read_ahead()

        data = self.__stream_buffer[:count]
        self.__collapse_head(count)

        return data

    def close(self):
        """
        Close the underlying socket.
        """
        self.close()
