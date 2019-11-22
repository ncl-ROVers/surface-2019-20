from PySide2.QtWidgets import *
from PySide2.QtGui import QTransform

_NORMAL_LEAK = 20
_NORMAL_TEMPERATURE = 30
_NORMAL_DEPTH = 3
_NORMAL_ACCELERATION = 5
_CRITICAL_LEAK = 50
_CRITICAL_TEMPERATURE = 50
_CRITICAL_DEPTH = 5
_CRITICAL_ACCELERATION = 10


class Indicator(QGraphicsScene):
    def __init__(self, normal, critical, name, unit, number):
        super(Indicator, self).__init__()
        self.normal = normal
        self.critical = critical
        self.name = name
        self.unit = unit
        self.number = number
        self.indicator = ('''Normal''', '''Attention''', '''Critical''')
        self.color = ('''157, 206, 209''', '''255, 150, 0''', '''255, 0, 0''')
        self.color_indicator = self.color[0]

        self._config()

    def _config(self):
        self._set_indicator()

    def _set_indicator(self):
        self._set_statue()
        self._set_html(self._color)
        self.text_name = QGraphicsTextItem()
        self.text_number = QGraphicsTextItem()
        self.text_indicator = QGraphicsTextItem()
        self.addItem(self.text_name)
        self.addItem(self.text_number)
        self.addItem(self.text_indicator)
        self.text_name.setHtml(self.html_name)
        self.text_number.setHtml(self.html_number)
        self.text_indicator.setHtml(self.html_indicator)
        self.text_name.setPos(45, 25)
        self.text_number.setPos(45, 50)
        self.text_indicator.setPos(45, 100)

    def _set_html(self, color):
        self.html_name = r'''
                         <p>
                            <span style="font-size: 24px; color: rgb(''' + color + ''');">''' + self.name + '''</span><br/>
                        </p>
                        '''
        self.html_number = r'''
                         <p>
                            <span style="font-size: 45px; color: rgb(''' + color + ''');">''' + str(
            self.number) + self.unit + '''</span><br/>
                        </p>
                        '''
        self.html_indicator = r'''
                            <p>
                            <span style="font-size: 20px; color: rgb(''' + color + ''');">''' + self._indicator + '''</span><br/>
                            </p>
                            '''

    def _set_statue(self):
        if self.number < self.normal:
            self._color = self.color[0]
            self._indicator = self.indicator[0]
        elif (self.number >= self.normal) & (self.number < self.critical):
            self._color = self.color[1]
            self._indicator = self.indicator[1]
        elif self.number >= self.critical:
            self._color = self.color[2]
            self._indicator = self.indicator[2]

    def _update(self, number):
        self.number = number
        self.clear()
        self._set_indicator()


class Leak_Sensor(Indicator):

    def __init__(self):
        super(Leak_Sensor, self).__init__(_NORMAL_LEAK, _CRITICAL_LEAK, "Leak Sensor", "%", 50)


class Temperature(Indicator):

    def __init__(self):
        super().__init__(_NORMAL_TEMPERATURE, _CRITICAL_TEMPERATURE, "Temperature", "℃", 32)


class Depth(Indicator):

    def __init__(self):
        super().__init__(_NORMAL_DEPTH, _CRITICAL_DEPTH, "Depth", "m", 3.5)


class Acceleration(Indicator):

    def __init__(self):
        super().__init__(_NORMAL_ACCELERATION, _CRITICAL_ACCELERATION, "Acceleration", "m/s2", 4.5)


class Rotation(QGraphicsScene):

    def __init__(self):
        super(Rotation, self).__init__()
        self.number_rotation_x = 30
        self.number_rotation_y = 65
        self.number_rotation_z = 27
        self._set_rotation()

    def _set_rotation(self):
        self._set_html()
        self.text_name = QGraphicsTextItem()
        self.text_x = QGraphicsTextItem()
        self.text_y = QGraphicsTextItem()
        self.text_z = QGraphicsTextItem()
        self.addItem(self.text_name)
        self.addItem(self.text_x)
        self.addItem(self.text_y)
        self.addItem(self.text_z)
        self.text_name.setHtml(self.html_name)
        self.text_x.setHtml(self.html_x)
        self.text_y.setHtml(self.html_y)
        self.text_z.setHtml(self.html_z)
        self.text_name.setPos(90, 30)
        self.text_x.setPos(50, 70)
        self.text_y.setPos(120, 70)
        self.text_z.setPos(70, 100)

    def _set_html(self):
        self.html_name = r'''
                         <p>
                            <span style="font-size: 24px; color: rgb(157, 206, 209);">Rotation</span><br/>
                        </p>
                        '''
        self.html_x = r'''
                         <p>
                            <span style="font-size: 24px; color: rgb(157, 206, 209);">X: ''' + str(
            self.number_rotation_x) + '''°</span><br/>
                        </p>
                        '''
        self.html_y = r'''
                         <p>
                            <span style="font-size: 24px; color: rgb(157, 206, 209);">Y: ''' + str(
            self.number_rotation_y) + '''°</span><br/>
                        </p>
                        '''
        self.html_z = r'''
                         <p>
                            <span style="font-size: 24px; color: rgb(157, 206, 209);">Z: ''' + str(
            self.number_rotation_z) + '''°</span><br/>
                        </p>
                        '''

    def _update(self, x, y, z):
        self.number_rotation_x = x
        self.number_rotation_y = y
        self.number_rotation_z = z
        self.clear()
        self._set_rotation()
        self.update()
