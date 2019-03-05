from PIL import Image, ImageDraw
import json
import os



infile = open("settings.json")
settings_dict = json.load(infile)

CANVAS_WIDTH = settings_dict["CANVAS_WIDTH"]
CANVAS_HEIGHT = settings_dict["CANVAS_HEIGHT"]
COLLAGE_WIDTH = settings_dict["COLLAGE_WIDTH"]
COLLAGE_HEIGHT = settings_dict["COLLAGE_HEIGHT"]

os.chdir("./photos/")

img_sample = input("input base size image: ")
img_in = Image.open(img_sample)

img_out = Image.new("RGB", (img_in.size[0]*CANVAS_WIDTH, img_in.size[1]*CANVAS_HEIGHT))

test_dir = os.listdir()

new_dir = []
for item in test_dir:
    if item[-5:] == ".jfif":
        new_dir.append(item)

new_dir.sort()
print(new_dir)

x_dir = []
x = 1
while x < 10:
    x_dir.append(str(x) + ".jfif")
    x += 1

x = 0
z = 1
while x < COLLAGE_HEIGHT:
    y = 0
    while y < COLLAGE_WIDTH:
        collage_part = Image.open(str(z) + ".jfif")
        img_out.paste(collage_part, ((y)*img_in.size[0], (x)*img_in.size[1]))
        collage_part.close()
        y += 1
        z += 1
    x += 1

os.chdir("../")
img_out.save("collage.png")

