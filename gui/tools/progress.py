import dearpygui.dearpygui as dpg

class ProgressBarVisualize():
    def __init__(self):
        self.current_progress = 0.00

    def progress(self):
        self.current_progress += self.progress_increment
        dpg.set_value("images_loading_bar", self.current_progress)
        dpg.configure_item("images_loading_bar", overlay=f"{round(self.current_progress*100, 2)}%")
        print(self.current_progress)

    def clear_progress(self):
        self.current_progress = 0.00
        dpg.set_value("images_loading_bar", 0)
        dpg.configure_item("images_loading_bar", overlay=f"{0}%")

    def update_value(self, desired_percentage, total_iterations):
        self.total_iterations = total_iterations
        self.desired_percentage = desired_percentage / 100
        self.progress_increment = self.desired_percentage / total_iterations
        dpg.set_value("progress_bar_hint", "Прогрес завантаження та об'єдання зображень")
    
    def end(self):
        self.current_progress = 1.00 - self.progress_increment
        self.progress()