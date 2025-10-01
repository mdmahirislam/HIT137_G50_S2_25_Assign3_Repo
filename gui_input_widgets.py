import tkinter as tk
from tkinter import ttk


class UserInputWidget:
    
    def __init__(self, main_window):
        # store the main window
        self.main_window = main_window
        
        # frame will be created later
        self.input_frame = None
        
        # tracks whether text or image is selected
        self.choice = tk.StringVar()
        self.choice.set("text")
        
        print("UserInputWidget created")
    
    def build_input_section(self):
        # create the frame with a title
        self.input_frame = ttk.LabelFrame(
            self.main_window, 
            text="User Input Section",
            padding=10
        )
        
        # frame is ready to use
        return self.input_frame