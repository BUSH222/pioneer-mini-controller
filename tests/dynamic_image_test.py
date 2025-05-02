import dearpygui.dearpygui as dpg
from PIL import Image
import time


image_path = "assets/camera_off.png"
image = Image.open(image_path).convert("RGBA")
width, height = image.size
image_data = list(image.getdata())
image_data = [c / 255.0 for pixel in image_data for c in pixel]


with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, image_data)


with dpg.window(label="dsafa"):
    dpg.add_image(texture_id)

dpg.create_viewport(title="nkfdjsabdh", width=width+40, height=height+60)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
time.sleep(10)
dpg.destroy_context()
