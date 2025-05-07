import cv2
import asyncio
import dearpygui.dearpygui as dpg
from pioneer_sdk import Camera
import numpy as np
import time
import threading
import requests

from .app_state import AppState
from .helper import generate_filename


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


async def take_picture(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        print("Pioneer not connected. Cannot take a picture.")
        return
    filename = generate_filename()
    data = requests.get(f'http://192.168.4.1/control?function=photo&name={filename}')
    print(data.json())
    return True


async def toggle_video_recording(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        print("Pioneer not connected. Cannot take a picture.")
        return
    if not app.video_recording:
        filename = generate_filename()
        data = requests.get(f'http://192.168.4.1/control?function=video_record&command=start&name={filename}')
        print(data.json())
        if not data.json()['success']:
            print('Something went wrong')
            return
        else:
            dpg.set_item_label(sender, "Stop video recording")
            app.video_recording = True
    else:
        data = requests.get('http://192.168.4.1/control?function=video_record&command=stop')
        print(data.json())
        if not data.json()['success']:
            print('Something went wrong')
            return
        else:
            dpg.set_item_label(sender, "Start video recording")
            app.video_recording = False
