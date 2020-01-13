"""
TODO: Document
"""
from .utils import Screen


class Sample(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        super(Sample, self).__init__()

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
        Display the menu bar as it should only be disabled in the loading screen.
        """
        super().on_switch()
        self.manager.bar.parent().setVisible(True)

    def on_exit(self):
        """
        Default inherited.
        """
        super().on_exit()
