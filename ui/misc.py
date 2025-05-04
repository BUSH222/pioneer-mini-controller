import dearpygui.dearpygui as dpg
import time
import math
import array

from core.app_state import AppState


def preload_camera_feed():
    texture_data = []
    for y in range(320):
        for x in range(480):
            r = (math.sin(x * 0.05) + 1) / 2
            g = (math.cos(y * 0.05) + 1) / 2
            b = (math.sin((x + y) * 0.02) + 1) / 2
            a = 1
            texture_data.append(r)
            texture_data.append(g)
            texture_data.append(b)
            texture_data.append(a)
    raw_data = array.array('f', texture_data)
    with dpg.texture_registry(show=True):
        dpg.add_raw_texture(
            width=480,
            height=320,
            default_value=raw_data,
            tag="camera_feed",
            format=dpg.mvFormat_Float_rgba
        )


def update_menubar():
    app = AppState()
    while True:
        if app.pioneer is not None and app.pioneer.connected():
            dpg.set_item_label("drone_status_menubar", "Drone: connected")
            if app.camera is None:
                dpg.set_item_label("camera_status_menubar", "Camera: disconnected")
            else:
                dpg.set_item_label("camera_status_menubar", "Camera: connected")
            battery = app.pioneer.get_battery_status(get_last_received=True)
            if battery is not None:
                dpg.set_item_label("battery_status_menubar", f"Battery: {battery:.2f} V")
            autopilot_state = app.pioneer.get_autopilot_state()
            if autopilot_state is None:
                dpg.set_item_label("autopilot_state_menubar", "Autopilot state: OFFLINE")
            else:
                dpg.set_item_label("autopilot_state_menubar", f"Autopilot state: {autopilot_state}")
            if autopilot_state is None or autopilot_state == 'IDLE':
                dpg.set_item_label("toggle_arm", "Arm propellers")

        else:
            dpg.set_item_label("drone_status_menubar", "Drone: disconnected")
            dpg.set_item_label("camera_status_menubar", "Camera: disconnected")
            dpg.set_item_label("autopilot_state_menubar", "Autopilot state: OFFLINE")
        time.sleep(2)
