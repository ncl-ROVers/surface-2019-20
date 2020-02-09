"""
TODO: Document
"""
from .utils import Screen


class Home(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        super(Home, self).__init__()

    def _config(self):
        """
        Default inherited.
        """
        super()._config()

    def _set_style(self):
        """
        Default inherited.
        """
        super()._set_style()

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        This screen is accessed immediately after the loading screen, hence it will have a lot of start-up
        functionalities. Currently the following are implemented:

            1. Display the menu bar (and the line break) as it should only be disabled in the loading screen.
            2. Start the connection check clock
        """
        super().on_switch()
        self.manager.bar.setVisible(True)
        self.manager.line_break.setVisible(True)
        self.manager.references.connection_clock.start()

    def on_exit(self):
        """
        Default inherited.
        """
        super().on_exit()
