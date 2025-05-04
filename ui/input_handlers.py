from core.app_state import AppState
import dearpygui.dearpygui as dpg


def handle_key_input():
    """Handles key inputs for throttle and RC controls."""
    app = AppState()

    def update_throttle(delta):
        app.throttle = max(0, min(1000, app.throttle + delta))  # Clamp throttle between 0 and 1000
        print(f"Throttle updated: {app.throttle}")

    def update_rc_controls(index, value):
        app.rc_controls[index] = value
        print(f"RC Controls updated: {app.rc_controls}")

    with dpg.handler_registry():
        # Throttle controls
        dpg.add_key_press_handler(key=dpg.mvKey_Shift, callback=lambda: update_throttle(50))  # Increase throttle
        dpg.add_key_press_handler(key=dpg.mvKey_Control, callback=lambda: update_throttle(-50))  # Decrease throttle

        # Pitch (W/S)
        dpg.add_key_press_handler(key=dpg.mvKey_W, callback=lambda: update_rc_controls(0, 1000))  # Forward
        dpg.add_key_release_handler(key=dpg.mvKey_W, callback=lambda: update_rc_controls(0, 0))  # Reset pitch
        dpg.add_key_press_handler(key=dpg.mvKey_S, callback=lambda: update_rc_controls(0, -1000))  # Backward
        dpg.add_key_release_handler(key=dpg.mvKey_S, callback=lambda: update_rc_controls(0, 0))  # Reset pitch

        # Roll (Q/E)
        dpg.add_key_press_handler(key=dpg.mvKey_Q, callback=lambda: update_rc_controls(1, -1000))  # Left roll
        dpg.add_key_release_handler(key=dpg.mvKey_Q, callback=lambda: update_rc_controls(1, 0))  # Reset roll
        dpg.add_key_press_handler(key=dpg.mvKey_E, callback=lambda: update_rc_controls(1, 1000))  # Right roll
        dpg.add_key_release_handler(key=dpg.mvKey_E, callback=lambda: update_rc_controls(1, 0))  # Reset roll

        # Yaw (A/D)
        dpg.add_key_press_handler(key=dpg.mvKey_A, callback=lambda: update_rc_controls(2, -1000))  # Left yaw
        dpg.add_key_release_handler(key=dpg.mvKey_A, callback=lambda: update_rc_controls(2, 0))  # Reset yaw
        dpg.add_key_press_handler(key=dpg.mvKey_D, callback=lambda: update_rc_controls(2, 1000))  # Right yaw
        dpg.add_key_release_handler(key=dpg.mvKey_D, callback=lambda: update_rc_controls(2, 0))  # Reset yaw
