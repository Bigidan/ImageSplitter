import os
from PIL import Image

def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return height, width
    except Exception as e:
        print(f"Помилка: {str(e)}")
        return None

def CountPageInfo(starting_page, required_N_pages, _chapter_path):
    page_sum = 0
    for i in range(starting_page, required_N_pages+1):
        print(f"{_chapter_path}Raw/{i}.jpg")
        curent_page = get_image_size(f"{_chapter_path}Raw/{i}.jpg")[0]
        page_sum += curent_page
    

    print(page_sum)
    return page_sum, get_image_size(f"{_chapter_path}Raw/{starting_page}.jpg")[1]

def GetBigImage(startImageNumber, endImageNumber, chapter_path):
    path = chapter_path

    bL, bW = CountPageInfo(startImageNumber, endImageNumber, chapter_path)
    BigImage = Image.new('RGB', (bW, bL))

    SmallImages = []
    for i in range(startImageNumber, endImageNumber+1):
        SmallImages.append([Image.open(f'{path}Raw/{i}.jpg'), get_image_size(f'{path}Raw/{i}.jpg')[0]])
    print()

    start_pos=0
    for y in range(len(SmallImages)):
        BigImage.paste(SmallImages[y][0], (0,start_pos))
        start_pos += SmallImages[y][1]
    return BigImage

def UniteImages(startImageNumber, endImageNumber, outName, _chapter_path):
    path = _chapter_path
    bL, bW = CountPageInfo(startImageNumber, endImageNumber, _chapter_path)
    bLL = bL/12000

    BigImage = GetBigImage(startImageNumber, endImageNumber, _chapter_path)

    if not os.path.exists(f"{path}tmp"):
        os.makedirs(f"{path}tmp")
    if not os.path.exists(f"{path}tmp/{outName}.png"):
        num_slices = int(bLL)
        slice_height = int(bL / num_slices)
        for i in range(num_slices):
            slice_name = f"{i+1}.png"
            start_y = i * slice_height
            end_y = (i + 1) * slice_height
            slice_img = BigImage.crop((0, start_y, bW, end_y))
            slice_img.save(f"{path}tmp/{slice_name}")
    return bL
def split_and_save_images(BigImage, separators, save_path):
    start_pos = 0
    index = 1
    if not os.path.exists(f"{save_path}/Split"):
        os.makedirs(f"{save_path}/Split")
    for separator in separators:
        end_pos = min(separator, BigImage.size[1])
        part_image = BigImage.crop((0, start_pos, BigImage.size[0], end_pos))
        part_image.save(f"{save_path}/Split/{index}.jpg")
        start_pos = separator
        index += 1

    sub_image = BigImage.crop((0, start_pos, BigImage.width, BigImage.height))
    sub_image.save(f"{save_path}/Split/{index}.jpg")

def ExportImages(startImageNumber, endImageNumber, chapter_path, separators):
    BigImage = GetBigImage(startImageNumber, endImageNumber, chapter_path)
    split_and_save_images(BigImage, separators, chapter_path)