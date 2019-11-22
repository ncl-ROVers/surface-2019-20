class Read_Data:
    def __init__(self, indicator):
        self.leak = 0
        self.temperature = 0
        self.depth = 0
        self.acceleration = 0
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.indicator = indicator
        self.on_process()

    def on_process(self):
        # self.read_data()  # This method is used in the real situation
        self._update()
        self.change_data()

    def read_data(self):
        """
        Assign the data to each parameters
        :return: null
        """
        self.leak = 0
        self.temperature = 0
        self.depth = 0
        self.acceleration = 0
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

    def change_data(self):
        """
        This is a test method
        :return:
        """
        self.leak += 1
        self.temperature += 1
        self.depth += 1
        self.acceleration += 1
        self.rotation_x += 1
        self.rotation_y += 1
        self.rotation_z += 1

    def _update(self):
        self.indicator.update_date(self.leak, self.temperature, self.depth, self.acceleration,
                                   self.rotation_x, self.rotation_y, self.rotation_z)
