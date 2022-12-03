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

#T: (dMin, dMax) -> (cMin, cMax) 
def transform(data: list, range:tuple):
    dMin = min(data)
    #print(dMin)
    dMax = max(data)
    #print(dMax)
    range_d = dMax - dMin
    range_c = range[1] - range[0]
    slope = float(range_c / range_d)
    print(slope)
    print(dMax*slope - slope*dMin)
    newData = []
    for value in data:
        newData.append(int(slope*value - slope*dMin + range[0]))
    
    return newData

#T: (1 x len(data)) -> (1 x dim)
def stretch_compress(data:list, dim:int):
    ratio = len(data) / dim
    newData = []
    for i in range(0, dim):
        newData.append(data[int(ratio*i)])
    assert(len(newData) == dim)

    return newData


    

def color_image(data, map, dim, cMin=None, cMax=None, func=None):
    print(data)
    if cMin == None:
        cMin = 0
    if cMax == None:
        cMax = len(map) - 1
    data = transform(data, (cMin, cMax))
    data = stretch_compress(data, dim)
    print(data)


colormap = matplotlib.cm.get_cmap("twilight").colors
colormap=denormalize(colormap)
data = []
for i in range(10, 1000):
    row = []
    for j in range(10, 1000):
        row.append(i)
    data.append(row)
color_image(data, colormap, 512, 100, 400)

# print(type(colormap))
# print(len(colormap))
# dim = 512
# #image = Image.new(mode="RGB", size=(dim, dim))
# pixels = []
# for i in range(dim):
#     row = []
#     for j in range(dim):
#         #print(colormap[i % len(colormap)])
#         row.append(tuple(colormap[i % len(colormap)]))
#     pixels.append(row)
# print(pixels)
# print(len(pixels))
# array = np.array(pixels, dtype=np.uint8)
# print(array)
# new_image = Image.fromarray(array)
# new_image.show()