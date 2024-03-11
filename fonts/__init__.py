import dearpygui.dearpygui as dpg

font_size = 17
default_path = './fonts/NotoSansMono-Regular.ttf'
font_registry = None
global_font = 0

def add_font(file, size: int | float, parent=0, **kwargs) -> int:
    if not isinstance(size, (int, float)):
        raise ValueError(f'font size must be an integer or float. Not {type(size)}')

    chars = ['▶', '×', '✖', '—', '■', '○', '↗']
    for i, char in enumerate(chars):
        chars[i] = ord(char)

    with dpg.font(file, size, default_font=True, parent=parent, **kwargs) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent=font)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=font)
        dpg.add_font_chars(chars, parent=font)
        dpg.add_font_chars([0x2514, 0x2502, 0x2500, 0x251C], parent=font)
    return font

def load() -> int:
    global font_registry, global_font

    font_registry = dpg.add_font_registry()
    global_font = add_font(default_path, font_size, parent=font_registry)
    return global_font