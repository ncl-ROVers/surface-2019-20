from PySide2.QtMultimedia import *


class Camera:

    def __init__(self):
        self.video_camera_1 = QCamera()
        self.video_camera_2 = QCamera()
        self.video_camera_3 = QCamera()
        self._config()

    def _config(self):
        self._set_video()
        pass

    def _set_video(self):
        """
        Set the camera device
        """

        pass

    def _camera_1(self):
        return self.video_camera_1

    def _camera_2(self):
        return self.video_camera_2

    def _camera_3(self):
        return self.video_camera_3
