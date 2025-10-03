import torch
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from transformers import CLIPTextModel, CLIPTokenizer, BlipProcessor, BlipForConditionalGeneration #This is not directly used but is used in the background for the diffusers library
from diffusers import DiffusionPipeline

class ModelGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Model GUI")
        self.geometry("1200x800")
        self.state("zoomed")

        self.create_menu()
        self.model_selection()
        self.input_output()
        self.info()

    def create_menu(self):
        menubar = tk.Menu(self)
        option_menu = tk.Menu(menubar, tearoff=0)
        option_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is a program which allows you to either generate images or describe an image using AI"))
        option_menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "Making an image may take a while."))
        option_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Options", menu=option_menu)
        self.config(menu=menubar)

    def model_selection(self):
        frame = tk.Frame(self, padx=20, pady=10)
        frame.pack(fill="x")
        tk.Label(frame, text="AI Model Generator", font=("Arial", 18) ).pack(side="left")

    
    def input_output(self):
        frame = tk.Frame(self, padx=20, pady=10)
        frame.pack(fill="both", expand=True)

        input_frame = tk.LabelFrame(frame, text="User Input")
        input_frame.pack(side="left", fill="both", expand=True)

        self.input_type = tk.StringVar(value="Text")  # radio button starts on Text input
        tk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text", command=self.input_update).pack(anchor="w")
        tk.Radiobutton(input_frame, text="Image", variable=self.input_type, value="Image", command=self.input_update).pack(anchor="w")

        self.input_box = scrolledtext.ScrolledText(input_frame, width=30, height=10)
        self.input_box.pack(fill="both", expand=True, pady=5)
        self.browse_btn = tk.Button(input_frame, text="Browse", command=self.browse)

        button_frame = tk.Frame(input_frame)
        button_frame.pack(side="bottom")

        # pass self into UserInput so it can grab text
        tk.Button(button_frame, text="Run Model", command =lambda: UserInput(self)).pack(side="left", pady=10, anchor="s")
        tk.Button(button_frame, text="Clear Input", command=self.input_update).pack(side="left", pady=10, padx=10, anchor="s")
        tk.Button(button_frame, text="Clear Output", command=lambda: self.output_display.delete("1.0", tk.END)).pack(side="left", pady=10, anchor="s")
        output_frame = tk.LabelFrame(frame, text="Model Output Section")
        output_frame.pack(side="left", fill="both", expand=True)

        tk.Label(output_frame, text="Output Display:").pack(anchor="w")
        self.output_display = scrolledtext.ScrolledText(output_frame, width=30, height=15)
        self.output_display.pack(fill="both", expand=True)

    def input_update(self):
        if self.input_type.get() == "Text":
            self.browse_btn.pack_forget()   # hide browse button
            self.input_box.pack(fill="both", expand=True, pady=5)  # show text box
            self.input_box.insert(tk.INSERT, "")
            self.input_box.configure(state="normal")
            self.input_box.delete("1.0", tk.END)
        else:
            self.input_box.pack_forget()   # hide text box
            self.browse_btn.pack(anchor="w", pady=2)  # show browse button
            self.input_box.pack(fill="both", expand=True, pady=5)  # show text box
            self.input_box.delete("1.0", tk.END)
            self.input_box.insert(tk.INSERT, "")
            self.input_box.configure(state="normal")
            self.input_box.delete("1.0", tk.END)
            self.input_box.configure(state="disabled")
            self.file_path = ""

    def info(self):
        frame = tk.LabelFrame(self, text = "Info and OOP Concepts Explanation")
        frame.pack(side="left", fill="both", expand=True, pady=10, padx=20)

        model_frame = tk.Frame(frame)
        model_frame.pack(side="left", fill="both", expand=True)

        tk.Label(
            model_frame,
            text="Ai Model Info:\nThe AI models chosen for this GUI is openjourney and Salesforce for text to image generation and image to text generation respectively.\nThe openjourney AI takes the users input in our GUI and generate an image based on the user’s prompt alone,\nthe more accurate the prompt the more accurate the image.\nThe main quality of life feature this AI has is it’s ability to filter inappropriate prompts.\nThis makes it safe to use in workplace environments and when used with children involved.\nSalesforce takes the users images and gives a description of the image to the best of its ability.\nThis can assist in describing images that might be odd and hard to describe.\nIf this AI is developed further, it can answer user questions about an image or potentially help the blind by describing an image in better detail to them making this applicable in multiple different scenarios.",
            wraplength=500,  # wrap text at 500px
            justify="left",
            anchor="w"
        ).pack(fill="both", expand=True, padx=10, pady=10)

        object_frame = tk.Frame(frame)
        object_frame.pack(side="left", fill="both", expand=True)

        tk.Label(
            object_frame,
            text="OOP Concepts:\nObject-oriented programming was heavily utilized as it allowed us to organise and optimise the code.\nInheritance was implemented by assigning the ModelGUI class the subclass tk.Tk allowing it to gain the functionality of a Tkinter window and other features.\nEncapsulation was also heavily utilized, using attributes such as self.input_type and self.input_box helped us keep the code organized.\nBreaking down parts of the GUI into sections such as create_menu() and model_selection() demonstrates modularity and helps us break problems down into more logical steps and made the code more organised.\nWe also created a separate class (prompt) which demonstrates a certain level of abstraction as that class was used for generating and displaying the images and texts.\nWe also demonstrated how to interact with different classes, through using the variable “app” to stand in for ModelGUI and using it in the prompt class.",
            wraplength=500,
            justify="left",
            anchor="w"
        ).pack(fill="both", expand=True, padx=10, pady=10)
        
    def browse(self):
        file_path = filedialog.askopenfilename(title="choose a file")
        if file_path:
            self.file_path = file_path
            img = Image.open(file_path); img.thumbnail((250,250))
            self.input_img_tk = ImageTk.PhotoImage(img)
            self.input_box.config(state="normal"); self.input_box.delete("1.0", tk.END)
            self.input_box.image_create(tk.END, image=self.input_img_tk)
            self.input_box.config(state="disabled")
    
     
#text to image
pipe = DiffusionPipeline.from_pretrained("prompthero/openjourney")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

#image to text
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda" if torch.cuda.is_available() else "cpu")

class prompt:
    def __init__(self, text):
        self.text = text

    def generate_image(self):
        image = pipe(self.text).images[0]
        return image
    
    def show(self):
        image = self.generate_image()
        image.show()


def UserInput(app):  # now takes the ModelGUI instance #"app" refers to modelGUI class
    input_type = app.input_type.get()
    text = app.input_box.get("1.0", tk.END).strip()  # get text from box
    if input_type == "Text":
        if not text:
            messagebox.showerror("Warning", "No text input detected!")
            return
        # Run the AI model
        p = prompt(text)
        image = p.generate_image()  # This is a PIL.Image object

        # Convert for Tkinter
        app.img_tk = ImageTk.PhotoImage(image)

        # Clear output before inserting
        app.output_display.delete("1.0", tk.END)

        # Insert image into output_display
        app.output_display.image_create(tk.END, image=app.img_tk)
        app.output_display.insert(tk.END, "\n")  # add spacing after
    elif input_type == "Image":
        if not hasattr(app, 'file_path') or not app.file_path:
            messagebox.showerror("Warning", "No image file selected!")
            return
        text = "This is a image of "

        inputs = processor(Image.open(app.file_path), return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

        out = model.generate(**inputs)
        app.output_display.delete("1.0", tk.END)
        app.output_display.insert(tk.INSERT, processor.decode(out[0], skip_special_tokens=True))




app = ModelGUI()
app.mainloop()