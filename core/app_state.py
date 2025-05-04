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
            cls._instance._throttle = 0
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
