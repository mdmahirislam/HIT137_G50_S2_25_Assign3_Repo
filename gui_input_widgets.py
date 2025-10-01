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
        # add radio buttons
        self.add_radio_buttons()
        # frame is ready to use
        return self.input_frame
    
    def add_radio_buttons(self):
        # create a row for radio buttons
        button_row = ttk.Frame(self.input_frame)
        button_row.pack(fill='x', pady=5)
        
        # text radio button
        text_btn = ttk.Radiobutton(
            button_row,
            text='Text',
            variable=self.choice,
            value='text'
        )
        text_btn.pack(side='left', padx=5)
        
        # image radio button  
        img_btn = ttk.Radiobutton(
            button_row,
            text='Image',
            variable=self.choice,
            value='image'
        )
        img_btn.pack(side='left', padx=5)
        
    