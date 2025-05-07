import asyncio
from pioneer_sdk import Pioneer
import dearpygui.dearpygui as dpg
import time

from .app_state import AppState
from .pioneer_extensions import send_manual_control

Pioneer.send_manual_control = send_manual_control


async def connect_to_drone(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        app.pioneer = Pioneer(logger=False, log_connection=False)
        await asyncio.sleep(0.1)
        for i in range(10):
            if not app.pioneer.connected():
                await asyncio.sleep(0.2)
                continue
            else:
                break
        if not app.pioneer.connected():
            dpg.set_item_label(sender, "Connect to Drone")
            print("Failed to connect to drone.")
        else:
            warn = app.pioneer.get_preflight_state()
            dpg.set_item_label(sender, "Disconnect from Drone")
            preflight_state_str = '\n'.join([f'{key}: {value}' for key, value in warn.items() if value is not None])
            if all(x is None for x in warn.values()):
                dpg.set_value("drone_preflight_logs", "No warnings! Everything is OK.")
            else:
                dpg.set_value("drone_preflight_logs", preflight_state_str)

    else:
        dpg.set_item_label(sender, "Connect to Drone")
        app.pioneer.close_connection()
        app.pioneer = None


async def set_led(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        print("Pioneer not connected. Cannot set LEDs.")
        return
    for i in range(4):
        rgb = dpg.get_value(f"led_{i}")
        r, g, b = [int(c) for c in rgb[:3]]
        if (r, g, b) == (1, 1, 1):
            r, g, b = 0, 0, 0
        if not app.pioneer.led_control(led_id=i, r=r, g=g, b=b):
            print(f"Failed to change LED {i} to {(r, g, b)}")


async def toggle_arm(sender, app_data, user_data):
    app = AppState()
    if app.pioneer is None:
        print("Pioneer not connected. Cannot arm.")
        return
    autopilot_state = app.pioneer.get_autopilot_state()
    if autopilot_state is None:
        print("Failed to get autopilot state.")
        return
    if autopilot_state == 'IDLE':
        app.pioneer.arm()
        dpg.set_item_label("toggle_arm", "Disarm propellers")
    else:
        app.pioneer.disarm()
        dpg.set_item_label("toggle_arm", "Arm propellers")


def control_mainloop():
    app = AppState()
    while True:
        if app.pioneer is not None and app.pioneer.connected():
            if app.control_mode == 'manual':
                rc_controls = app.rc_controls
                throttle = app.throttle
                try:
                    app.pioneer.send_manual_control(
                        x=rc_controls[0],  # Pitch
                        y=rc_controls[1],  # Roll
                        z=throttle,        # Throttle
                        r=rc_controls[2],  # Yaw
                        buttons=0          # No buttons pressed
                    )
                except Exception as e:
                    print(f"Failed to send manual control: {e}")
            elif app.control_mode == 'stab':
                velocities = app.stab_velocities
                try:
                    app.pioneer.set_manual_speed(*velocities)
                except Exception as e:
                    print(f"Failed to send manual control: {e}")
        time.sleep(0.1)


async def takeoff(sender, app_data, user_data):
    app = AppState()
    if app.control_mode == 'manual':
        app.throttle = 450
    elif app.control_mode == 'stab':
        app.pioneer.takeoff()


async def land(sender, app_data, user_data):
    app = AppState()
    app.pioneer.land()
