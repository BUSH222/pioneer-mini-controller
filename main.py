import dearpygui.dearpygui as dpg
from pioneer_sdk import Pioneer, Camera
import asyncio
import threading
from core.helper import acw, start_background_loop
from ui.layout import (preload_camera_feed,
                       resize_main_window,
                       update_sidebar_width,
                       save_sidebar_width)
import time
import cv2
import numpy as np

threading.Thread(target=start_background_loop, daemon=True).start()

dpg.create_context()


pioneer = None
camera = None
video_running = False
print("Pioneer SDK initialized.")

# Preload the camera feed
preload_camera_feed()


async def connect_to_drone(sender, app_data, user_data):
    global pioneer
    if pioneer is None:
        pioneer = Pioneer(logger=False, log_connection=False)
        await asyncio.sleep(0.1)
        for i in range(10):
            if not pioneer.connected():
                await asyncio.sleep(0.2)
                continue
            else:
                break
        if not pioneer.connected():
            dpg.set_item_label(sender, "Connect to Drone")
            print("Failed to connect to drone.")
        else:
            warn = pioneer.get_preflight_state()
            dpg.set_item_label(sender, "Disconnect from Drone")
            preflight_state_str = '\n'.join([f'{key}: {value}' for key, value in warn.items() if value is not None])
            if all(x is None for x in warn.values()):
                dpg.set_value("drone_preflight_logs", "No warnings! Everything is OK.")
            else:
                dpg.set_value("drone_preflight_logs", preflight_state_str)

    else:
        dpg.set_item_label(sender, "Connect to Drone")
        pioneer.close_connection()
        pioneer = None


async def connect_to_camera(sender, app_data, user_data):
    global camera, video_running, pioneer
    if pioneer is None:
        dpg.set_item_label(sender, "Connect to Camera")
        print("Pioneer not connected. Cannot connect to camera.")
        return
    if camera is None:
        camera = Camera(log_connection=False)
        await asyncio.sleep(0.5)
        if camera.connect():
            dpg.set_item_label(sender, "Disconnect from Camera")
            video_running = True

            def video_loop():
                while video_running:
                    raw_frame = camera.get_frame()
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
            print("Failed to connect to camera.")
    else:
        dpg.set_item_label(sender, "Connect to Camera")
        video_running = False
        camera.disconnect()
        camera = None


async def set_led(sender, app_data, user_data):
    if pioneer is None:
        print("Pioneer not connected. Cannot set LEDs.")
        return
    for i in range(4):
        rgb = dpg.get_value(f"led_{i}")
        r, g, b = [int(c) for c in rgb[:3]]
        if (r, g, b) == (1, 1, 1):
            r, g, b = 0, 0, 0
        if not pioneer.led_control(led_id=i, r=r, g=g, b=b):
            print(f"Failed to change LED {i} to {(r, g, b)}")


def update_pioneer_status():
    global pioneer, camera
    while True:
        if pioneer is not None and pioneer.connected():
            dpg.set_item_label("drone_status_menubar", "Drone: connected")
            if camera is None:
                dpg.set_item_label("camera_status_menubar", "Camera: disconnected")
            else:
                dpg.set_item_label("camera_status_menubar", "Camera: connected")
            battery = pioneer.get_battery_status(get_last_received=True)
            if battery is not None:
                dpg.set_item_label("battery_status_menubar", f"Battery: {battery:.2f} V")
        else:
            dpg.set_item_label("drone_status_menubar", "Drone: disconnected")
            dpg.set_item_label("camera_status_menubar", "Camera: disconnected")
        time.sleep(5)


def main():
    with dpg.window(label="Main Window", tag="Main Window",
                    no_move=True, no_resize=True, no_collapse=True, no_close=True, no_scrollbar=True):
        # Top Navbar
        with dpg.menu_bar():
            dpg.add_menu_item(label="Battery: ?? V", tag="battery_status_menubar")
            dpg.add_menu_item(label="Drone: disconnected", tag="drone_status_menubar")
            dpg.add_menu_item(label="Camera: disconnected", tag="camera_status_menubar")

        # Horizontal layout for Sidebar and Main Content Area
        with dpg.group(horizontal=True):
            # Sidebar
            with dpg.child_window(width=300, tag="Sidebar"):
                with dpg.collapsing_header(label="Connection Window", default_open=True):
                    dpg.add_text("No warnings to display", tag="drone_preflight_logs")
                    dpg.add_button(label="Connect to Drone", callback=acw(connect_to_drone))
                    dpg.add_button(label="Connect to Camera", callback=acw(connect_to_camera))
                with dpg.collapsing_header(label="Control Window", default_open=False):
                    dpg.add_text("Control options go here.")

                with dpg.collapsing_header(label="Record Window", default_open=False):
                    dpg.add_text("Recording settings go here.")

                with dpg.collapsing_header(label="LED Control", default_open=False):
                    dpg.add_color_picker(label="LED 0", tag="led_0",
                                         default_value=(1.0, 1.0, 1.0, 1.0),
                                         no_alpha=True,
                                         picker_mode=dpg.mvColorPicker_wheel)
                    dpg.add_color_picker(label="LED 1", tag="led_1",
                                         default_value=(1.0, 1.0, 1.0, 1.0),
                                         no_alpha=True,
                                         picker_mode=dpg.mvColorPicker_wheel)
                    dpg.add_color_picker(label="LED 2", tag="led_2",
                                         default_value=(1.0, 1.0, 1.0, 1.0),
                                         no_alpha=True,
                                         picker_mode=dpg.mvColorPicker_wheel)
                    dpg.add_color_picker(label="LED 3", tag="led_3",
                                         default_value=(1.0, 1.0, 1.0, 1.0),
                                         no_alpha=True,
                                         picker_mode=dpg.mvColorPicker_wheel)
                    dpg.add_button(label="Set LEDs", callback=acw(set_led))

                with dpg.collapsing_header(label="UI", default_open=False):
                    dpg.add_slider_int(
                        label="Sidebar Width",
                        default_value=300,
                        min_value=100,
                        max_value=500,
                        callback=update_sidebar_width
                    )

                    dpg.add_button(label="Apply", callback=save_sidebar_width)

            # Main Content Area
            with dpg.child_window(width=800, height=500, tag="Main Content"):
                dpg.add_image("camera_feed")

    # Background threads:
    threading.Thread(target=update_pioneer_status, daemon=True).start()

    dpg.create_viewport(title="Drone Flight Control", width=1000, height=600)
    dpg.set_viewport_resize_callback(resize_main_window)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    resize_main_window(None, None)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
