class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._pioneer = None
            cls._instance._camera = None
            cls._instance._video_running = False
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
