import os
from PIL import Image
from .progress import ProgressBarVisualize
import dearpygui.dearpygui as dpg
from natsort import natsorted

progress_manager = ProgressBarVisualize()
def get_files_extention():
    return dpg.get_value("chapter_extention")

def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return height, width
    except Exception as e:
        dpg.set_value("error_text", f"Вхідні дані: {image_path}\nПомилка: {str(e)}")
        dpg.configure_item("modal_id", show=True)
        return None

def CountPageInfo(sorted_image_files, _chapter_path):
    global progress_manager
    page_sum = 0
    progress_manager.update_value(12.67, len(sorted_image_files))
    progress_manager.clear_progress()
    for image_file in sorted_image_files:
        print(image_file)
        curent_page = get_image_size(os.path.join(_chapter_path, "Raw", image_file))[0]
        page_sum += curent_page
        progress_manager.progress()
    
    print(page_sum)
    print("CountPageInfo end")
    return page_sum, get_image_size(os.path.join(_chapter_path, "Raw", sorted_image_files[0]))[1]

def GetBigImage(startImageNumber, endImageNumber, chapter_path):
    path = chapter_path

    sorted_image_files = natsorted(os.listdir(os.path.join(path, "Raw")))
    print("ТАК:\t")
    print(sorted_image_files)

    bL, bW = CountPageInfo(sorted_image_files, chapter_path)
    BigImage = Image.new('RGB', (bW, bL))

    SmallImages = []
    for image_file in sorted_image_files:
        SmallImages.append([Image.open(os.path.join(path, "Raw", image_file)), get_image_size(os.path.join(path, "Raw", image_file))[0]])
        print("Зображення\t" + image_file)

    start_pos=0
    for y in range(len(SmallImages)):
        BigImage.paste(SmallImages[y][0], (0,start_pos))
        start_pos += SmallImages[y][1]
    return BigImage, bL, bW

def UniteImages(startImageNumber, endImageNumber, outName, _chapter_path):
    global progress_manager
    path = _chapter_path

    BigImage, bL, bW = GetBigImage(startImageNumber, endImageNumber, _chapter_path)
    bLL = bL/12000

    

    if not os.path.exists(f"{path}tmp"):
        os.makedirs(f"{path}tmp")
    if not os.path.exists(f"{path}tmp/{outName}.png"):
        num_slices = int(bLL)
        slice_height = int(bL / num_slices)
        progress_manager.update_value(39.53, num_slices)
        for i in range(num_slices):
            slice_name = f"{i+1}.png"
            start_y = i * slice_height
            end_y = (i + 1) * slice_height
            slice_img = BigImage.crop((0, start_y, bW, end_y))
            slice_img.save(f"{path}tmp/{slice_name}")
            progress_manager.progress()
    else:
        progress_manager.update_value(24.88, 1)
        progress_manager.progress()
    print("UniteImages end")
    return bL
def split_and_save_images(BigImage, separators, save_path):
    start_pos = 0
    index = 1
    if not os.path.exists(f"{save_path}/Split"):
        os.makedirs(f"{save_path}/Split")
    for separator in separators:
        end_pos = min(separator, BigImage[0].size[1])
        part_image = BigImage[0].crop((0, start_pos, BigImage[0].size[0], end_pos))
        part_image.save(f"{save_path}/Split/{index}.{get_files_extention()}")
        start_pos = separator
        index += 1

    sub_image = BigImage[0].crop((0, start_pos, BigImage[0].width, BigImage[0].height))
    sub_image.save(f"{save_path}/Split/{index}.{get_files_extention()}")

def ExportImages(startImageNumber, endImageNumber, chapter_path, separators):
    BigImage = GetBigImage(startImageNumber, endImageNumber, chapter_path)
    split_and_save_images(BigImage, separators, chapter_path)