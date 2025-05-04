import dearpygui.dearpygui as dpg

from core.app_state import AppState


def resize_main_window(sender, app_data):
    app = AppState()
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("Main Window", width)
    dpg.set_item_height("Main Window", height)
    sidebar_height = height - 55
    main_content_width = width - app.sidebar_width - 25
    main_content_height = height - 55

    dpg.set_item_width("Sidebar", app.sidebar_width)
    dpg.set_item_height("Sidebar", sidebar_height)
    dpg.set_item_width("Main Content", main_content_width)
    dpg.set_item_height("Main Content", main_content_height)


def update_sidebar_width(sender, app_data):
    app = AppState()
    app.sidebar_width = app_data


def save_sidebar_width(sender, app_data):
    app = AppState()
    dpg.set_item_width("Sidebar", app.sidebar_width)
    dpg.set_item_width("Main Content", dpg.get_viewport_client_width() - app.sidebar_width)
