import matplotlib.cm
import matplotlib
import numpy as np
from PIL import Image
#colormap = matplotlib.cm.get_cmap("viridis").colors
# pixels = [
#    [(54, 54, 54), (232, 23, 93), (71, 71, 71), (168, 167, 167)],
#    [(204, 82, 122), (54, 54, 54), (168, 167, 167), (232, 23, 93)],
#    [(71, 71, 71), (168, 167, 167), (54, 54, 54), (204, 82, 122)],
#    [(168, 167, 167), (204, 82, 122), (232, 23, 93), (54, 54, 54)]
# ]

# # Convert the pixels into an array using numpy
# array = np.array(pixels, dtype=np.uint8)
# print(array)
# # Use PIL to create an image from the new array of pixels
# new_image = Image.fromarray(array)
# new_image.show()


# exit()

def denormalize(palette):
    return [  
        tuple(int(channel * 255) for channel in color)
        for color in palette
    ]

colormap = matplotlib.cm.get_cmap("twilight").colors
colormap=denormalize(colormap)
print(type(colormap))
print(len(colormap))
dim = 512
#image = Image.new(mode="RGB", size=(dim, dim))
pixels = []
for i in range(dim):
    row = []
    for j in range(dim):
        #print(colormap[i % len(colormap)])
        row.append(tuple(colormap[i % len(colormap)]))
    pixels.append(row)
print(pixels)
print(len(pixels))
array = np.array(pixels, dtype=np.uint8)
print(array)
new_image = Image.fromarray(array)
new_image.show()