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
        
        # add text box
        self.add_text_input()
        
        # add action buttons
        self.add_action_buttons()
        
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
        
        # attach file button
        browse_btn = ttk.Button(
            button_row,
            text='Attach a File',
            command=self.handle_browse
        )
        browse_btn.pack(side='left', padx=10)
    
    def handle_browse(self):
        # open file dialog to select a file
        from tkinter import filedialog
        
    
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("All Files", "*.*")]
        )
        
        if file_path:
            print("Selected file:", file_path)
            # store the file path
            self.selected_file = file_path
        else:
            print("No file selected")
        
    def add_text_input(self):
        
        # used scrolledtext to create bigger text box
        from tkinter import scrolledtext
        
        # make the text box where user types
        self.text_area = scrolledtext.ScrolledText(
            self.input_frame,
            height=4,
            width=30,
            wrap='word'
        )
        self.text_area.pack(pady=10, anchor="w")
    
    def add_action_buttons(self):
        # frame for buttons at bottom
        button_frame = ttk.Frame(self.input_frame)
        button_frame.pack(fill='x', pady=10)
        
        # model 1 button
        run1_btn = ttk.Button(
            button_frame,
            text='Model 1',
            command=self.run_model_1
        )
        run1_btn.pack(side='left', padx=5)
        
        # model 2 button
        run2_btn = ttk.Button(
            button_frame,
            text='Model 2',
            command=self.run_model_2
        )
        run2_btn.pack(side='left', padx=5)

    def run_model_1(self):
        # placeholder
        print("Model 1 clicked")

    def run_model_2(self):
        # placeholder
        print("Model 2 clicked")
        
        

        
        

    