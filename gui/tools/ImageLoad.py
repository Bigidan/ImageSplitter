import dearpygui.dearpygui as dpg

from .file_manage import CountPagesNumb
from .ImagePhoto import UniteImages
from .ImagePhoto import progress_manager

def AddImagesToView(user_data):
    separator_manager, __multiplier, __mimimultiplier = user_data
    separator_manager.clear_all_separators()
    chapter_path = dpg.get_value("chapter_path")
    if chapter_path.endswith("/") or chapter_path.endswith("\\"):
        pass
    else:
        chapter_path += "/"
    if not (bool(chapter_path and not chapter_path.isspace())):
        return
    
    page_numb = CountPagesNumb(chapter_path, "Raw")
    
    bL = UniteImages(1, page_numb, 1, chapter_path)
    parts = []

    dpg.delete_item("drawlist_id", children_only=True)
    dpg.delete_item("navbar_list_id", children_only=True)
    dpg.delete_item("mininavbar_list_id", children_only=True)

    pp = CountPagesNumb(chapter_path)+1
    progress_manager.update_value(39.14, pp*2)
    for i in range(1, pp):
        print(f"1: {i}")
        parts.append(dpg.load_image(chapter_path + f"tmp/{i}.png"))
        progress_manager.progress()
    with dpg.texture_registry():
        index = 0
        for i in parts:
            width, height, channels, data = i
            dpg.delete_item(f"image_id_{index}")
            dpg.add_static_texture(width, height, data, tag=f"image_id_{index}")
            index += 1
            print(f"2: {i}")
            progress_manager.progress()

    index = 0
    pos_x = 0
    for i in parts:
        im_width, im_height, channels, data = i
        dpg.draw_image(f"image_id_{index}", (0, pos_x), (im_width, pos_x+im_height), uv_min=(0, 0), uv_max=(1, 1), parent="drawlist_id")
        dpg.draw_image(f"image_id_{index}", (0, pos_x*__multiplier), (im_width*__multiplier, (pos_x+im_height)*__multiplier), uv_min=(0, 0), uv_max=(1, 1), parent="navbar_list_id")
        dpg.draw_image(f"image_id_{index}", (0, pos_x*__mimimultiplier), (im_width*__mimimultiplier, (pos_x+im_height)*__mimimultiplier), uv_min=(0, 0), uv_max=(1, 1), parent="mininavbar_list_id")
        pos_x += im_height
        index += 1
    progress_manager.end()
    dpg.configure_item("drawlist_id", width=im_width, height=bL)

    dpg.configure_item("navbar_list_id", width=im_width*__multiplier+100, height=bL*__multiplier)
    dpg.configure_item("window_navbar_list_id", width=im_width*__multiplier+100)

    dpg.configure_item("mininavbar_list_id", width=im_width*__mimimultiplier+100, height=bL*__mimimultiplier)
    dpg.configure_item("window_mininavbar_list_id", width=im_width*__mimimultiplier+100)
    print("AddImagesToView end")
    return bL

def Export(separator_manager):
    separator_manager.export()