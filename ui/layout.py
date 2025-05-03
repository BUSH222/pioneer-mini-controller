import dearpygui.dearpygui as dpg
import math
import array

sidebar_width = 300


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


def resize_main_window(sender, app_data):
    global sidebar_width
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("Main Window", width)
    dpg.set_item_height("Main Window", height)
    sidebar_height = height - 55
    main_content_width = width - sidebar_width - 25
    main_content_height = height - 55

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
