import tkinter as tk
from tkinter import ttk

class ControlSection:
    def __init__(self, parent):
        self.parent = parent
        self.control_frame = None
        self.selected_model = tk.StringVar()
    
    def build_control_section(self):
        # control frame for dropdown and button
        self.control_frame = ttk.Frame(self.parent, padding=10)
        
        # frame for model selection stuff
        model_frame = ttk.Frame(self.control_frame)
        model_frame.pack(side='left', padx=10)
        
        # label
        ttk.Label(model_frame, text="Model Selection:").pack(side='left', padx=5)
        
        # dropdown for models
        self.model_dropdown = ttk.Combobox(
            model_frame,
            textvariable=self.selected_model,
            values=["Text Generation", "Image Classification"],
            state="readonly",
            width=20
        )
        self.model_dropdown.pack(side='left', padx=5)
        self.model_dropdown.current(0)
        
        # load button
        self.load_btn = ttk.Button(
            self.control_frame,
            text="Load Model",
            command=self.load_model
        )
        self.load_btn.pack(side='left', padx=10)
        
        return self.control_frame
    
    def load_model(self):
        print(f"Loading {self.selected_model.get()}")