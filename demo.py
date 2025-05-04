# Standalone Dear PyGui script to debug key handling
import dearpygui.dearpygui as dpg

def debug_key_input():
    """Debug key inputs to identify the correct key values."""
    with dpg.handler_registry():
        # Print key value when a key is pressed
        dpg.add_key_down_handler(callback=lambda sender, app_data: print(f"Key Down: {app_data}"))
        # Print key value when a key is released
        dpg.add_key_release_handler(callback=lambda sender, app_data: print(f"Key Released: {app_data}"))


def main():
    dpg.create_context()

    # Create a simple window
    with dpg.window(label="Key Debugger", width=400, height=200):
        dpg.add_text("Press any key to see its value in the console.")
        dpg.add_text("Use this to identify the correct key values for your system.")

    # Register the key debug handler
    debug_key_input()

    dpg.create_viewport(title="Key Debugger", width=400, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
