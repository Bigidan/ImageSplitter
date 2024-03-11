import dearpygui.dearpygui as dpg
import fonts

dpg.create_context()

dpg.bind_font(fonts.load())


def start():
    import gui
    main_window = gui.MainWindow()
    dpg.set_primary_window(main_window.window, True)

dpg.set_frame_callback(2, start)
dpg.setup_dearpygui()
dpg.create_viewport(title='Image Splitter by Bigidun', width=1700, height=900, small_icon="./icon.ico", large_icon="./icon.ico")

dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()