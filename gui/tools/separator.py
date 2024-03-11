from .file_manage import CountPagesNumb
from .ImagePhoto import ExportImages

import dearpygui.dearpygui as dpg

class SeparatorManager:
    def __init__(self):
        self.__separators = []
        self.mouse_pos = []
        self.scroll_offset = 0
        self.multiplier = 0.2
        self.mini_multiplier = 0.1
        self.chapter_path = ""

    def change_pos(self, pos):
        self.mouse_pos = pos
    def set_path(self, path):
        chapter_path = path
        if chapter_path.endswith("/") or chapter_path.endswith("\\"):
            pass
        else:
            chapter_path += "/"
        if not (bool(chapter_path and not chapter_path.isspace())):
            return
        
        self.chapter_path = chapter_path
    

    def clear_all_separators(self):
        dpg.delete_item("separators_list", children_only=True)
        all_items_allieases = dpg.get_aliases()
        for i in all_items_allieases:
            if "list_id" in i:
                if "L_" in i or "T_" in i or "A_" in i:
                    dpg.delete_item(f"{i}")
        self.__separators.clear()
        self.display_separator_table()

    def draw_separator(self, x, parent_name, name, mult=1):
        dpg.draw_line((0, x), (1000 * mult, x), color=(37, 37, 38, 255), thickness=4, parent=parent_name, tag=f"L_{parent_name}_{int(name)}")
        dpg.draw_arrow((500 * mult, x - 4), (1000 * mult, x - 200), color=(255, 0, 0, 255), thickness=3, size=14, parent=parent_name, tag=f"A_{parent_name}_{int(name)}")
        dpg.draw_text((400 * mult, x - 35), name, color=(255, 0, 0, 255), size=int(30 * mult), parent=parent_name, tag=f"T_{parent_name}_{int(name)}")

    def auto_separate(self, user_data):
        padd = int(dpg.get_value("auto_separator_padding"))
        print(padd)
        print(user_data)
        if (padd > 13999) or (padd < 4000):
            return
        i = padd
        while i < user_data:
            self.separator(auto_separator=True, auto_x=i)
            i += padd

    def separator(self, auto_separator=False, auto_x=0):
        if not auto_separator:
            mouse_pos = self.mouse_pos
        else:
            mouse_pos = [300.0, auto_x]
        if 1.0 < mouse_pos[0] < 710.0 and mouse_pos[1] > 1.0:
            name = self.scroll_offset - 35 + mouse_pos[1]
            self.draw_separator(self.scroll_offset - 35 + mouse_pos[1], "drawlist_id", name)
            self.draw_separator((self.scroll_offset - 35 + mouse_pos[1]) * self.multiplier, "navbar_list_id", name, self.multiplier)
            self.draw_separator((self.scroll_offset - 35 + mouse_pos[1]) * self.mini_multiplier, "mininavbar_list_id", name, self.mini_multiplier)

            self.__separators.append(name)
            self.__separators.sort()
            self.display_separator_table()

    def dedraw_separator(self, name):
        for el in ['L', 'A', 'T']:
            for par in ['drawlist_id', 'navbar_list_id', 'mininavbar_list_id']:
                dpg.delete_item(f"{el}_{par}_{int(name)}")

    def delete_separator(self, sender, app_data, user_data):
        self.dedraw_separator(f'{int(user_data)}')
        self.__separators.remove(user_data)
        self.display_separator_table()

    def display_separator_table(self):
        dpg.delete_item("separators_list", children_only=True)
        with dpg.table(header_row=True, parent="separators_list", no_host_extendY=True, height=300,
                       borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True,
                       row_background=True, scrollY=True):
            dpg.add_table_column(label="Висота")
            dpg.add_table_column(label="Відрізок")
            dpg.add_table_column(label="Видалити")
            prev_sep = 0
            for current_sep_height in self.__separators:
                with dpg.table_row():
                    dpg.add_selectable(label=f"{current_sep_height}", span_columns=False,
                                       callback=self.clb_selectable, user_data=current_sep_height)
                    dpg.add_text(f"{abs(prev_sep - current_sep_height)}")
                    dpg.add_button(label="x", user_data=current_sep_height, callback=self.delete_separator)
                prev_sep = current_sep_height

            pages = len(self.__separators) + 1
            dpg.set_value("separaters_count", f"Розділювачів: {len(self.__separators)}\tСторінок: {pages}")

    def clb_selectable(self, sender, app_data, user_data):
        if float(user_data) < 401:
            window_scroll_pos = 0
        else:
            window_scroll_pos = float(user_data) - 400
        dpg.set_y_scroll("window_drawlist_id", window_scroll_pos)
        dpg.set_y_scroll("window_mininavbar_list_id", window_scroll_pos * self.mini_multiplier)

    def navigator_box(self, pm):
        dpg.configure_item("mininav_rel", pmin=(pm[0], pm[1]+5), pmax=(pm[0]+85, pm[1]+93))
    def _scroll(self, sender, app_data, user_data):
        """
        Виконує паралельне гортання вікон. 
        `user_data` приймає назву вікна, яке гортається
        """
        if user_data[0] == "window_drawlist_id":
            scroll_data = [["window_drawlist_id", 1], ["window_navbar_list_id" , self.multiplier], ["window_mininavbar_list_id", self.mini_multiplier]]
        
        elif user_data[0] == "window_navbar_list_id":
            scroll_data = [["window_navbar_list_id", self.multiplier], ["window_drawlist_id" , 1/self.multiplier], ["window_mininavbar_list_id", 1/self.multiplier*self.mini_multiplier]]
        
        else:
            scroll_data = [["window_mininavbar_list_id", self.mini_multiplier], ["window_drawlist_id" , 1/self.mini_multiplier], ["window_navbar_list_id", 1/self.mini_multiplier*self.multiplier]]

        with dpg.mutex():
            y_scroll = dpg.get_y_scroll(scroll_data[0][0])
            if dpg.get_active_window() == dpg.get_alias_id(scroll_data[0][0]) and self.scroll_offset != y_scroll*scroll_data[0][1]:
                dpg.set_y_scroll(scroll_data[1][0], y_scroll*scroll_data[1][1])
                dpg.set_y_scroll(scroll_data[2][0], y_scroll*scroll_data[2][1])
                self.scroll_offset = y_scroll*scroll_data[0][1]
                self.navigator_box(pm=dpg.get_item_pos("window_mininavbar_list_id"))
    def export(self):
        if len(self.__separators) > 1:
            ExportImages(1, CountPagesNumb(self.chapter_path, "Raw"), self.chapter_path, self.__separators)