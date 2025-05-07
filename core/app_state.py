class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._pioneer = None
            cls._instance._camera = None
            cls._instance._video_running = False
            cls._instance._sidebar_width = 300
            cls._instance._background_loop = None
            cls._instance._rc_controls = [0, 0, 0]
            cls._instance._throttle = 100  # drone is in ground effect at around 450
            cls._instance._video_recording = False  # record onto the SD card
            cls._instance._control_mode = 'manual'  # manual or stab
            cls._instance._stab_velocities = [0, 0, 0, 0]  # vx, vy, vz, yaw_rate
        return cls._instance

    @property
    def pioneer(self):
        return self._pioneer

    @pioneer.setter
    def pioneer(self, value):
        self._pioneer = value

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def video_running(self):
        return self._video_running

    @video_running.setter
    def video_running(self, value):
        self._video_running = value

    @property
    def sidebar_width(self):
        return self._sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value):
        self._sidebar_width = value

    @property
    def background_loop(self):
        return self._background_loop

    @background_loop.setter
    def background_loop(self, value):
        self._background_loop = value

    @property
    def rc_controls(self):
        return self._rc_controls

    @rc_controls.setter
    def rc_controls(self, value):
        self._rc_controls = value

    @property
    def throttle(self):
        return self._throttle

    @throttle.setter
    def throttle(self, value):
        self._throttle = value

    @property
    def video_recording(self):
        return self._video_recording

    @video_recording.setter
    def video_recording(self, value):
        self._video_recording = value

    @property
    def control_mode(self):
        return self._control_mode

    @control_mode.setter
    def control_mode(self, value):
        self._control_mode = value

    @property
    def stab_velocities(self):
        return self._stab_velocities

    @stab_velocities.setter
    def stab_velocities(self, value):
        self._stab_velocities = value
