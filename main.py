import dearpygui.dearpygui as dpg
import threading

from core.helper import start_background_loop
from core.drone_controller import control_mainloop
from ui.resize import resize_main_window
from ui.misc import update_menubar, preload_camera_feed
from ui.layout import draw_layout
from ui.input_handlers import handle_key_input


def main():
    # Background loop thread for async functions
    threading.Thread(target=start_background_loop, daemon=True).start()
    dpg.create_context()

    # Preload the camera feed
    preload_camera_feed()

    # Draw the layout
    draw_layout()

    # Register key handlers
    handle_key_input()

    # Background threads:
    threading.Thread(target=update_menubar, daemon=True).start()  # Update the menubar every 5 seconds
    threading.Thread(target=control_mainloop, daemon=True).start()  # Control the drone every 0.1 seconds

    dpg.create_viewport(title="Drone Flight Control", width=1000, height=600)
    dpg.set_viewport_resize_callback(resize_main_window)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    resize_main_window(None, None)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
