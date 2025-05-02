import dearpygui.dearpygui as dpg
from PIL import Image


image_path = "assets/camera_off.png"
image = Image.open(image_path).convert("RGBA")
width, height = image.size
image_data = list(image.getdata())
image_data = [c / 255.0 for pixel in image_data for c in pixel]

print('entry to tex reg')
with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, image_data)
print('prepping window')

with dpg.window(label="dsafa"):
    dpg.add_image(texture_id)
print('prepping create viewport')

dpg.create_viewport(title="nkfdjsabdh", width=width+40, height=height+60)
print('a')
dpg.setup_dearpygui()
print('b')
dpg.show_viewport()
print('c')
dpg.start_dearpygui()
print('d')
dpg.destroy_context()
print('e')
