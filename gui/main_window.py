import dearpygui.dearpygui as dpg
from .tools.separator import SeparatorManager
from .tools.ImageLoad import AddImagesToView as AtV
from .tools.ImageLoad import Export as ImE

separator_manager = SeparatorManager()
big_image_height = 0

def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)
def _hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (255*v, 255*t, 255*p)
    if i == 1: return (255*q, 255*v, 255*p)
    if i == 2: return (255*p, 255*v, 255*t)
    if i == 3: return (255*p, 255*q, 255*v)
    if i == 4: return (255*t, 255*p, 255*v)
    if i == 5: return (255*v, 255*p, 255*q)

def callback(sender, app_data):
    dpg.set_value("chapter_path", f"{app_data['file_path_name']}")
    print('Обрано папку')

def cancel_callback(sender, app_data):
    print('Скасовано')
    #print("Sender: ", sender)
    #print("App Data: ", app_data)

def set_lenght(value):
    global big_image_height
    big_image_height = value
    
    separator_manager.set_path(dpg.get_value("chapter_path"))

def auto_images():
    global big_image_height
    separator_manager.auto_separate(big_image_height)

def export():
    ImE(separator_manager)

class MainWindow():
    window: int = 0

    def __init__(self):
        super().__init__()
        dpg.add_viewport_drawlist(front=True, tag="viewport_back")
        dpg.draw_rectangle((0, 0), (0, 0), color=(255, 0, 0, 255), thickness=2, parent="viewport_back", tag="mininav_rel")

        with dpg.window(label="Error handle", modal=True, show=False, tag="modal_id", no_title_bar=True, autosize=True):
            dpg.add_text("Помилка", tag="error_text")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Oк", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))

        with dpg.window() as self.window:
            _text_id = dpg.add_text("Велике вікно")
            with dpg.table(header_row=False, resizable=True, delay_search=True, borders_outerH=False, borders_innerV=True, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(border=False, tag="window_drawlist_id"):
                        with dpg.drawlist(width=100, height=100, tag="drawlist_id"):
                            pass
                    with dpg.item_handler_registry(tag="__demo_item_reg0"):
                            dpg.add_item_visible_handler(user_data=["window_drawlist_id"], callback=separator_manager._scroll)
                    dpg.bind_item_handler_registry(_text_id, dpg.last_container())

                    with dpg.group(horizontal=False):
                        _text_id2 = dpg.add_text("Програма для склеювання та розрізання зображень манхв")
                        _text_id3 = dpg.add_text("Рекомендована структура папок:\n"
                                    "├───Chapters\n"
                                    "│   ├───chapter-1\n"
                                    "│   │   ├───Raw\n"
                                    "│   │   └───Translated\n"
                                    "│   └───chapter-2\n"
                                    "│       ├───Raw\n"
                                    "│       └───Translated\n")
                        with dpg.group(horizontal=True):
                            dpg.add_input_text(label="Папка із зображеннями", hint="Шлях", tag="chapter_path")
                            
                            dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
                                                cancel_callback=cancel_callback, width=1000, height=700)
                            dpg.add_button(label="Огляд", callback=lambda: dpg.show_item("file_dialog_id"))
                            _help(
                                    "Уведення:\n"
                                    "Для коректної роботи шлях потрібно вводити у форматі:\n"
                                    "С:/MangaName/Chapters/chapter-1/\n"
                                    "або\n"
                                    "С:\\MangaName\\Chapters\\chapter-1\\\n"
                                    "Можна скористатися кнопкою Огляду.\n\n")
                            
                        dpg.add_input_text(label="розширення фалів, яке буде на виході\n(без крапки)", hint="Шлях", tag="chapter_extention", default_value="webp")
                        dpg.add_button(label="Завантажити", user_data=[separator_manager, 0.2, 0.1], callback=lambda s, a, u: set_lenght(AtV(u)))

                        with dpg.group(horizontal=True):
                            dpg.add_progress_bar(label="Обробка...", tag="images_loading_bar", default_value=0.0, overlay="0%")
                            with dpg.tooltip(dpg.last_item()):
                                dpg.add_text("Отака хуйня, малята", tag="progress_bar_hint")
                            dpg.add_text("Обробка зображень")

                        with dpg.group(horizontal=True):
                            with dpg.child_window(border=True, tag="window_navbar_list_id"):
                                with dpg.drawlist(width=100, height=100, tag="navbar_list_id"):
                                    pass

                            with dpg.item_handler_registry(tag="__demo_item_reg1"):
                                dpg.add_item_visible_handler(user_data=["window_navbar_list_id"], callback=separator_manager._scroll)
                            dpg.bind_item_handler_registry(_text_id2, dpg.last_container())

                            with dpg.child_window(border=True, tag="window_mininavbar_list_id"):
                                with dpg.drawlist(width=100, height=100, tag="mininavbar_list_id"):
                                    pass
                            with dpg.item_handler_registry(tag="__demo_item_reg2"):
                                dpg.add_item_visible_handler(user_data=["window_mininavbar_list_id"], callback=separator_manager._scroll)
                            dpg.bind_item_handler_registry(_text_id3, dpg.last_container())

                            with dpg.handler_registry(show=False, tag="__demo_mouse_handler"):
                                m_release = dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left)
                                m_drag = dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left)
                                m_down = dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left)
                                m_move = dpg.add_mouse_move_handler()
                                m_click = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left)
                            
                            with dpg.group(horizontal=False):
                                dpg.add_checkbox(label="Активувати додавання розділювачі мишою", callback=lambda s, a: dpg.configure_item("__demo_mouse_handler", show=a))
                                _help(
                                        "Пояснення:\n"
                                        "Коли увімкнено, можна розставляти розділювачі\n"
                                        "затискаючи Shift та натискаючи лівою клавішею\n"
                                        "миші у Великому вікні.\n")
                                mh_click = dpg.add_text("Mouse id:", label="Mouse Click Handler", show_label=True)
                                mh_release = dpg.add_text("Mouse id:", label="Mouse Release Handler", show_label=True)
                                mh_drag = dpg.add_text("Mouse id:  delta:", label="Mouse Drag Handler", show_label=True)
                                with dpg.group(horizontal=True):
                                    dpg.add_button(label="Автоматично", user_data=big_image_height, callback=auto_images)
                                    _help(
                                        "Пояснення:\n"
                                        "Натискання цієї кнопки розставити розділювачі\n"
                                        "з кроком у вказану кількість пікселів.\n"
                                        "Від 4000 до 14000.\n"
                                        "Це НЕ видалить усі попередні розділювачі.\n"
                                        "Зауважте:\n"
                                        "Програма ніяк не обробляє місце розділювача,\n"
                                        "тому я рекомендую використовувати їх як\n"
                                        "навігаційні якорі для швидкого переміщення\n"
                                        "та розставляння їх вручну.\n\n"
                                        "Рекомендується переглянути відео.\n\n")
                                    dpg.add_slider_int(label="Відступ", tag="auto_separator_padding", width=200,
                                                    default_value=9000, max_value=13990, min_value=4000)

                                with dpg.group(horizontal=False, tag="separators_list"):
                                    pass
                                dpg.add_text("Розділювачів: 0\tСторінок: 0", tag="separaters_count")
                                _help(
                                        "Пояснення:\n"
                                        "У цій таблиці відображається висота(пікселі)\n"
                                        "розділювача, різниця в пікселях від попереднього,\n"
                                        "та кнопка для його видалення.\n"
                                        "Зауважте:\n"
                                        "Натискання на ім'я перемістить перегляд усіх\n"
                                        "віконець на цей розідлювач.\n"
                                        "Використовуйте це для швидкого переміщення.\n\n")
                                dpg.add_button(label="Очистити ВСЕ", callback=separator_manager.clear_all_separators)
                                with dpg.theme(tag="__demo_theme"):
                                    i = 3
                                    with dpg.theme_component(dpg.mvButton):
                                        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(i/7.0, 0.6, 0.6))
                                        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(i/7.0, 0.8, 0.8))
                                        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(i/7.0, 0.7, 0.7))
                                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, i*5)
                                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, i*3, i*3)
                                    
                                dpg.add_button(label="Експортувати", callback=export)
                                dpg.bind_item_theme(dpg.last_item(), "__demo_theme")
                                separator_manager.display_separator_table()

                            def _event_handler(sender, data):
                                type=dpg.get_item_info(sender)["type"]
                                if type=="mvAppItemType::mvMouseClickHandler":
                                    dpg.set_value(mh_click, f"Mouse id: {data} + Shift: {dpg.is_key_down(dpg.mvKey_Shift)}")
                                    if dpg.is_key_down(dpg.mvKey_Shift):
                                        separator_manager.separator()
                                elif type=="mvAppItemType::mvMouseReleaseHandler":
                                    dpg.set_value(mh_release, f"Mouse id: {data}")
                                elif type=="mvAppItemType::mvMouseMoveHandler":
                                    separator_manager.change_pos(pos=data)
                                    global __mouse_pos
                                    __mouse_pos = data
                                    print(__mouse_pos)
                                elif type=="mvAppItemType::mvMouseDragHandler":
                                    dpg.set_value(mh_drag, f"Mouse id: {data[0]}, Delta:{[data[1], data[2]]}")

                            for handler in dpg.get_item_children("__demo_mouse_handler", 1):
                                dpg.set_item_callback(handler, _event_handler)