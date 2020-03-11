"""
Connection
==========

Module storing an implementation of a socket-based connection with the ROV.
"""
import socket as _socket
import json as _json
import multiprocessing as _mp
import threading as _threading
from .utils import ConnectionStatus as _ConnectionStatus
from ..common import data_manager as _dm
from ..common import Log as _Log


class Connection:
    """
    Connection class used as a two-way data exchange medium.

    Handles sending transmission data to ROV and receiving information back.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create and initialise socket and process related constructs
        * status - a getter to retrieve current connection status
        * connected - a getter to check if the communication is still happening
        * connect - a method used to connect with the ROV (spawns separate thread)
        * _connect - a method used to connect with the ROV
        * disconnect - a method used to disconnect with the ROV
        * reconnect - a helper method used to disconnect and connect in one step
        * _communicate - a private method which does the actual communication with the ROV (send and recv)
        * _new_socket - a private method which re-initialises the socket
        * _new_process - a private method which re-initialises the process
        * _cleanup - a private method used to (attempt to) clean-up the resources

    Usage
    -----

    The connection should be created as follows::

        connection = Connection()
        connection.connect()

    While working, the code should check if the communication is happening, to detect when it stops::

        if not connection.connected():
            connection.reconnect()

    Once finished, to cleanup the resources, a disconnection should happen::

        connection.disconnect()

    Note that the operating system should be capable of cleaning up any incorrectly closed sockets (upon
    server-initiated disconnection, the sockets must (at least) go into the TIME_WAIT state), but the processes will not
    be cleaned and persist as zombie processes.

    .. warning::

        The calling functions must handle when the attempts to connect, disconnect etc. should be made, and detect when
        the communication stops (for example by checking the status). This is NOT handled internally.
    """

    def __init__(self, ip: str = "localhost", *, port: int = 50000):
        """
        Standard constructor.

        Initialises the socket and the process, as well as sets the initial status of the connection as `DISCONNECTED`.

        :param ip: Ip of the server to connect to
        :param port: Port to connect to
        """
        self._ip = ip
        self._port = port
        self._address = self._ip, self._port

        # Initialise the socket and the connection status
        self._socket = self._new_socket()
        self._status = _ConnectionStatus.DISCONNECTED

        # Initialise the process for sending and receiving the data
        self._process = self._new_process()

    @property
    def status(self) -> _ConnectionStatus:
        """
        Getter for the connection status.
        """
        return self._status

    @property
    def connected(self) -> bool:
        """
        Getter to check if the communication is happening.
        """
        return self._process.is_alive()

    def connect(self):
        """
        Helper method used to connect in a non-blocking way (separate thread)
        """
        _threading.Thread(target=self._connect).start()

    def _connect(self):
        """
        Method used to connect to the server and start exchanging the data.

        The steps are as follows:

            1. Set the status to `CONNECTING`
            2. Attempt to connect the client and the server sockets
            3. Start the communication process
            4. Set the status to `CONNECTED`

        On errors, the status is set to `DISCONNECTED` and the cleanup function is called.
        """
        if self._status != _ConnectionStatus.DISCONNECTED:
            _Log.error(f"Can't connect to {self._ip}:{self._port} - not disconnected (status is {self._status.name})")
            return

        _Log.info(f"Connecting to {self._ip}:{self._port}...")
        self._status = _ConnectionStatus.CONNECTING
        try:
            self._socket.connect(self._address)
            _Log.info(f"Connected to {self._ip}:{self._port}")
            self._status = _ConnectionStatus.CONNECTED
            self._process.start()
        except (ConnectionError, OSError) as e:
            _Log.error(f"Failed to connect to {self._ip}:{self._port} - {e}")
            self._status = _ConnectionStatus.DISCONNECTED
            self._cleanup(ignore_errors=True)

    def disconnect(self):
        """
        Method used to disconnect from the server and stop exchanging the data.

        Performs the cleanup and sets the status to `DISCONNECTED` on success, or leaves the status in its current state
        on errors.
        """
        if self._status != _ConnectionStatus.CONNECTED:
            _Log.error(f"Can't disconnect from {self._ip}:{self._port} - not connected "
                       f"(status is {self._status.name})")
            return

        _Log.info(f"Disconnecting from {self._ip}:{self._port}...")
        try:
            self._cleanup()
            _Log.info(f"Disconnected from {self._ip}:{self._port}")
            self._status = _ConnectionStatus.DISCONNECTED
        except (ConnectionError, OSError) as e:
            _Log.error(f"Failed to disconnect from {self._ip}:{self._port} - {e}")

    def reconnect(self):
        """
        Method used to reconnect to the server (disconnect and connect).
        """
        _Log.info(f"Reconnecting to {self._ip}:{self._port}...")
        self.disconnect()
        self.connect()

    def _communicate(self):
        """
        Function used to exchange the data with the server.

        Being a separate process, it is safe to let this function run in an infinite while loop, because to stop this
        communication it is sufficient to stop (terminate) the process (OS-level interruption).

        Breaks the infinite loop on errors, leaving the calling code to accommodate for errors.
        """
        while True:
            try:
                _Log.debug("Fetching data for transmission")
                data = _dm.transmission.get_all()

                # Encode the transmission data as JSON and send the bytes to the server
                _Log.debug(f"Sending transmission data - {data}")
                self._socket.sendall(bytes(_json.dumps(data), encoding="utf-8"))

                _Log.debug("Receiving transmission data")
                data = self._socket.recv(4096)

                # Exit if connection closed by server
                if not data:
                    _Log.info("Connection closed by server")
                    break

                try:
                    data = _json.loads(data.decode("utf-8").strip())
                except (UnicodeError, _json.JSONDecodeError) as e:
                    _Log.debug(f"Failed to decode following data: {data} - {e}")
                    break

                # Only handle valid, non-empty data
                if data and isinstance(data, dict):
                    _Log.debug(f"Received the following data - {data}")
                    _dm.received.update(data)

            except (ConnectionError, OSError) as e:
                _Log.error(f"An error occurred while communicating with the server - {e}")
                break

    def _new_socket(self) -> _socket.socket:
        """
        Function used as a default socket generator.

        :return: New, correctly configured socket object
        """
        return _socket.socket()

    def _new_process(self) -> _mp.Process:
        """
        Function used as a default communication process generator.

        :return: New, correctly configured process object
        """
        return _mp.Process(target=self._communicate)

    def _cleanup(self, ignore_errors: bool = False):
        """
        Method used to cleanup the connection and the communication process.

        The steps are as follows:

            1. Terminate the process (if it's alive)
            2. Create a new process
            3. Shutdown and close the socket
            4. Create a new socket

        Errors can be optionally ignored with the `ignore_errors` flag.

        :param ignore_errors: Boolean determining whether the errors should be propagated or not
        """
        try:
            if self._process.is_alive():
                self._process.terminate()
            self._process = self._new_process()
            self._socket.shutdown(_socket.SHUT_RDWR)
            self._socket.close()
            self._socket = self._new_socket()
        except (ConnectionError, OSError) as e:
            if not ignore_errors:
                raise e
            else:
                _Log.debug(f"Connection ignoring the following error - {e}")
