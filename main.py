import dearpygui.dearpygui as dpg
from pioneer_sdk import Pioneer, Camera
import array
import math
import asyncio
import threading
from helper import acw, start_background_loop


threading.Thread(target=start_background_loop, daemon=True).start()

dpg.create_context()

sidebar_width = 300
pioneer = None
camera = None
print("Pioneer SDK initialized.")


# Preload the camera feed
texture_data = []
for y in range(320):
    for x in range(480):
        r = (math.sin(x * 0.05) + 1) / 2
        g = (math.cos(y * 0.05) + 1) / 2
        b = (math.sin((x + y) * 0.02) + 1) / 2
        a = 1  # Fully opaque
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


def resize_main_window(sender, app_data):
    global sidebar_width
    """Callback to resize the main window and its child elements when the viewport is resized."""
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("Main Window", width)
    dpg.set_item_height("Main Window", height)
    sidebar_height = height - 30
    main_content_width = width - sidebar_width
    main_content_height = height - 30

    dpg.set_item_width("Sidebar", sidebar_width)
    dpg.set_item_height("Sidebar", sidebar_height)
    dpg.set_item_width("Main Content", main_content_width)
    dpg.set_item_height("Main Content", main_content_height)


def update_sidebar_width(sender, app_data):
    global sidebar_width
    sidebar_width = app_data


def save_sidebar_width(sender, app_data):
    global sidebar_width
    dpg.set_item_width("Sidebar", sidebar_width)
    dpg.set_item_width("Main Content", dpg.get_viewport_client_width() - sidebar_width)


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
            dpg.set_item_label(sender, "Disconnect from Drone")
    else:
        dpg.set_item_label(sender, "Connect to Drone")
        pioneer.close_connection()
        pioneer = None


async def connect_to_camera(sender, app_data, user_data):
    global camera
    if pioneer is None:
        dpg.set_item_label(sender, "Connect to Camera")
        print("Pioneer not connected. Cannot connect to camera.")
        return
    if camera is None:
        camera = Camera(log_connection=False)
        await asyncio.sleep(0.5)
        if camera.connect():
            dpg.set_item_label(sender, "Disconnect from Camera")
        else:
            dpg.set_item_label(sender, "Connect to Camera")
            print("Failed to connect to camera.")
    else:
        dpg.set_item_label(sender, "Connect to Camera")
        camera.disconnect()
        camera = None


def main():
    with dpg.window(label="Main Window", tag="Main Window",
                    no_move=True, no_resize=True, no_collapse=True, no_close=True, no_scrollbar=True):
        # Top Navbar
        with dpg.menu_bar():
            dpg.add_menu_item(label="Battery: ?? V")
            dpg.add_menu_item(label="Warnings: None")

        # Horizontal layout for Sidebar and Main Content Area
        with dpg.group(horizontal=True):
            # Sidebar
            with dpg.child_window(width=300, height=500, tag="Sidebar"):
                with dpg.collapsing_header(label="Connection Window", default_open=True):
                    dpg.add_text("Connection status goes here.")
                    dpg.add_button(label="Connect to Drone", callback=acw(connect_to_drone))
                    dpg.add_button(label="Connect to Camera", callback=acw(connect_to_camera))
                with dpg.collapsing_header(label="Control Window", default_open=True):
                    dpg.add_text("Control options go here.")

                with dpg.collapsing_header(label="Record Window", default_open=True):
                    dpg.add_text("Recording settings go here.")

                with dpg.collapsing_header(label="UI", default_open=True):
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

    dpg.create_viewport(title="Drone Flight Control", width=1000, height=600)
    resize_main_window(None, None)
    dpg.set_viewport_resize_callback(resize_main_window)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()