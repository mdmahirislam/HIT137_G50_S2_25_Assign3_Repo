import tkinter as tk
from gui_control_section import ControlSection

# create window
window = tk.Tk()
window.title("Test Control Section")
window.geometry("600x200")

# create control section
control = ControlSection(window)
frame = control.build_control_section()
frame.pack(fill='x', padx=10, pady=10)

# run
window.mainloop()