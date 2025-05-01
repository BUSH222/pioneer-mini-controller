import dearpygui.dearpygui as dpg


def resize_main_window(sender, app_data):
    """Callback to resize the main window and its child elements when the viewport is resized."""
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("Main Window", width)
    dpg.set_item_height("Main Window", height)

    # Adjust the height of the sidebar and main content area
    sidebar_width = 200  # Fixed width for the sidebar
    sidebar_height = height - 30  # Subtracting space for the menu bar
    main_content_width = width - sidebar_width  # Remaining width for the main content area
    main_content_height = height - 30

    dpg.set_item_width("Sidebar", sidebar_width)
    dpg.set_item_height("Sidebar", sidebar_height)
    dpg.set_item_width("Main Content", main_content_width)
    dpg.set_item_height("Main Content", main_content_height)


def update_sidebar_width(sender, app_data):
    dpg.set_item_width("Sidebar", app_data)
    dpg.set_item_width("Main Content", dpg.get_viewport_client_width() - app_data)


def main():
    dpg.create_context()

    with dpg.window(label="Main Window", tag="Main Window",
                    no_move=True, no_resize=True, no_collapse=True, no_close=True, no_scrollbar=True):
        # Top Navbar
        with dpg.menu_bar():
            dpg.add_menu_item(label="Battery: 100%")
            dpg.add_menu_item(label="Warnings: None")
            dpg.add_menu_item(label="Notifications: 0")

        # Horizontal layout for Sidebar and Main Content Area
        with dpg.group(horizontal=True):
            # Sidebar
            with dpg.child_window(width=200, height=500, tag="Sidebar"):
                with dpg.collapsing_header(label="Connection Window", default_open=True):
                    dpg.add_text("Connection status goes here.")

                with dpg.collapsing_header(label="Control Window", default_open=True):
                    dpg.add_text("Control options go here.")

                with dpg.collapsing_header(label="Record Window", default_open=True):
                    dpg.add_text("Recording settings go here.")

                with dpg.collapsing_header(label="UI", default_open=True):
                    dpg.add_slider_int(
                        label="Sidebar Width",
                        default_value=200,
                        min_value=100,
                        max_value=400,
                        callback=update_sidebar_width
                    )

            # Main Content Area
            with dpg.child_window(width=800, height=500, tag="Main Content"):
                dpg.add_text("Main content area goes here.")

    dpg.create_viewport(title="Drone Flight Control", width=1000, height=600)
    resize_main_window(None, None)
    dpg.set_viewport_resize_callback(resize_main_window)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
