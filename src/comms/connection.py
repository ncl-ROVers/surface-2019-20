"""
TODO: Document
"""
import socket as _socket
import json as _json
import time as _time
import multiprocessing as _mp
from .utils import ConnectionStatus as _ConnectionStatus
from ..common import data_manager as _dm
from ..common import Log as _Log


class Connection:
    """
    TODO: Document
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

    def connect(self):
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
            _Log.error(f"Can't' connect to {self._ip}:{self._port} - not disconnected (status is {self._status.name})")
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
            _Log.error(f"Can't' disconnect from {self._ip}:{self._port} - not connected "
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
        """
        while True:
            pass

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
