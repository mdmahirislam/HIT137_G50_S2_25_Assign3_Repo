# tools/make_samples.py
from PIL import Image, ImageDraw, ImageFont

def draw_apple(size=512, save_path="apple.jpg"):
    img = Image.new("RGB", (size, size), "white")
    d = ImageDraw.Draw(img)
    d.ellipse((size*0.2, size*0.2, size*0.8, size*0.8), fill=(220, 30, 30))  # body
    d.ellipse((size*0.52, size*0.08, size*0.72, size*0.24), fill=(34, 139, 34))  # leaf
    d.rectangle([size*0.48, size*0.1, size*0.52, size*0.2], fill=(139,69,19))   # stem
    d.ellipse((size*0.3, size*0.78, size*0.7, size*0.86), fill=(160, 20, 20))   # shadow
    try:
        font = ImageFont.load_default()
        d.text((10, size-20), "apple", fill="black", font=font)
    except:
        pass
    img.save(save_path, "JPEG", quality=90)

def draw_mug(size=512, save_path="mug.jpg"):
    img = Image.new("RGB", (size, size), "white")
    d = ImageDraw.Draw(img)
    left, top, right, bottom = size*0.25, size*0.25, size*0.65, size*0.78
    r = int(size*0.05)
    d.rectangle([left+r, top, right-r, bottom], fill=(210,210,210))
    d.rectangle([left, top+r, right, bottom-r], fill=(210,210,210))
    d.pieslice([left, top, left+2*r, top+2*r], 180, 270, fill=(210,210,210))
    d.pieslice([right-2*r, top, right, top+2*r], 270, 360, fill=(210,210,210))
    d.pieslice([left, bottom-2*r, left+2*r, bottom], 90, 180, fill=(210,210,210))
    d.pieslice([right-2*r, bottom-2*r, right, bottom], 0, 90, fill=(210,210,210))
    # handle
    hx1, hy1, hx2, hy2 = right, size*0.35, size*0.85, size*0.68
    d.ellipse([hx1, hy1, hx2, hy2], outline=(170,170,170), width=int(size*0.03))
    d.ellipse([hx1+size*0.03, hy1+size*0.03, hx2-size*0.03, hy2-size*0.03], outline=(255,255,255), width=int(size*0.02))
    # coffee
    d.ellipse((left+size*0.02, top+size*0.04, right-size*0.02, top+size*0.18), fill=(120,72,0))
    # shadow
    d.ellipse((size*0.2, size*0.8, size*0.8, size*0.9), fill=(220,220,220))
    try:
        font = ImageFont.load_default()
        d.text((10, size-20), "mug", fill="black", font=font)
    except:
        pass
    img.save(save_path, "JPEG", quality=90)

if __name__ == "__main__":
    draw_apple()
    draw_mug()
    print("Created apple.jpg and mug.jpg")
