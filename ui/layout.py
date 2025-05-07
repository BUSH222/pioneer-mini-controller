import dearpygui.dearpygui as dpg

from core.helper import acw
from core.drone_controller import connect_to_drone, set_led, toggle_arm
from core.camera_controller import connect_to_camera, take_picture, toggle_video_recording
from ui.resize import update_sidebar_width, save_sidebar_width


def draw_layout():
    with dpg.window(label="Main Window", tag="Main Window",
                    no_move=True, no_resize=True, no_collapse=True, no_close=True, no_scrollbar=True):
        # Top Navbar
        with dpg.menu_bar():
            dpg.add_menu_item(label="Battery: ?? V", tag="battery_status_menubar")
            dpg.add_menu_item(label="Drone: disconnected", tag="drone_status_menubar")
            dpg.add_menu_item(label="Camera: disconnected", tag="camera_status_menubar")
            dpg.add_menu_item(label="Autopilot state: OFFLINE", tag="autopilot_state_menubar")

        # Horizontal layout for Sidebar and Main Content Area
        with dpg.group(horizontal=True):
            # Sidebar
            with dpg.child_window(width=300, tag="Sidebar"):
                with dpg.collapsing_header(label="Connection Window", default_open=True):
                    dpg.add_text("No warnings to display", tag="drone_preflight_logs")
                    dpg.add_button(label="Connect to Drone", callback=acw(connect_to_drone))
                    dpg.add_button(label="Connect to Camera", callback=acw(connect_to_camera))
                with dpg.collapsing_header(label="Control Window", default_open=False):
                    dpg.add_button(label="Arm propellers", tag="toggle_arm", callback=acw(toggle_arm))
                    dpg.add_text("Control options go here.")

                with dpg.collapsing_header(label="Record Window", default_open=False):
                    dpg.add_button(label="Take picture", tag="take_picture", callback=acw(take_picture))
                    dpg.add_button(label="Start video recording", tag="toggle_recording",
                                   callback=acw(toggle_video_recording))
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
