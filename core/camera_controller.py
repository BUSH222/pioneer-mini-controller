import cv2
import asyncio
import dearpygui.dearpygui as dpg
from pioneer_sdk import Camera
import numpy as np
import time
import threading

from .app_state import AppState


async def connect_to_camera(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        dpg.set_item_label(sender, "Connect to Camera")
        print("Pioneer not connected. Cannot connect to app.camera.")
        return
    if app.camera is None:
        app.camera = Camera(log_connection=False)
        await asyncio.sleep(0.5)
        if app.camera.connect():
            dpg.set_item_label(sender, "Disconnect from Camera")
            app.video_running = True

            def video_loop():
                while app.video_running:
                    raw_frame = app.camera.get_frame()
                    if raw_frame is not None:
                        frame = cv2.imdecode(np.frombuffer(raw_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
                        frame = cv2.resize(frame, (480, 320))
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                        float_data = frame.astype(np.float32) / 255.0
                        dpg.set_value("camera_feed", float_data.flatten())
                    time.sleep(0.03)
            threading.Thread(target=video_loop, daemon=True).start()

        else:
            dpg.set_item_label(sender, "Connect to Camera")
            print("Failed to connect to app.camera.")
    else:
        dpg.set_item_label(sender, "Connect to Camera")
        app.video_running = False
        app.camera.disconnect()
        app.camera = None
