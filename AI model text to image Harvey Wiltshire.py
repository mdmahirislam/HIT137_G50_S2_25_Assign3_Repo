from transformers import CLIPTextModel, CLIPTokenizer #This is not directly used but is used in the background for the diffusers library
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("prompthero/openjourney")
pipe = pipe.to("cuda")

class prompt:
    def __init__(self, text):
        self.text = text

    def generate_image(self):
        image = pipe(self.text).images[0]
        return image
    
    def show(self):
        image = self.generate_image()
        image.show()
        image.save("generated_image.png")#This is the image that will be saved to the same directory as the code file if u need to change the image type for tkinter

def UserInput(): #assign this to the generate image button
    text = input("Enter your prompt: ") #change the input only to take in the user input from the GUI make sure it is still text = ________ when finished
    p = prompt(text)
    p.show()

UserInput()#once the object above has a button assigned to it, remove this line
