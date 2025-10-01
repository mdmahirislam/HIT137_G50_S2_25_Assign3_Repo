import tkinter as tk
from gui_input_widgets import UserInputWidget

# create main window
window = tk.Tk()
window.title("Testing My Input Widget")
window.geometry("500x400")

# create your widget
my_widget = UserInputWidget(window)

# build and display it
input_section = my_widget.build_input_section()
input_section.pack(fill='both', expand=True, padx=20, pady=20)

# run the window
window.mainloop()