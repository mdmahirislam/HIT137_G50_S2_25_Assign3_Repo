import torch

from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")

raw_image = ["generated_image.png"]

text = "a photography of"

inputs = processor(raw_image, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))