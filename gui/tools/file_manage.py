import os
import dearpygui.dearpygui as dpg

def CountPagesNumb(chapter_path, path="tmp"):
    try:
        count_file=0
        for path in os.scandir(f"{chapter_path}/{path}/"):
            if path.is_file():
                count_file += 1
        return count_file
    except Exception as e:
        print(e)
        dpg.set_value("error_text", f"Помилка під час перерахунку відних файлів:\n{str(e)}")
        dpg.configure_item("modal_id", show=True)