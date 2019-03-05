from PIL import Image, ImageDraw
import json
import os

img_sample = input("input base size image: ")
img_in = Image.open(img_sample)

img_out = Image.new("RGB", (img_in.size[0]*6, img_in.size[1]*3))

test_dir = os.listdir()

dict_file = open("images.json")
img_dict = json.load(dict_file)

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
while x < 3:
    y = 0
    while y < 3:
        collage_part = Image.open(str(z) + ".jfif")
        img_out.paste(collage_part, ((y)*img_in.size[0], (x)*img_in.size[1]))
        collage_part.close()
        y += 1
        z = (z + 1) % 5
	if z == 0:
	    z += 1
    x += 1


img_out.save("collage.png")

