import matplotlib.cm
import matplotlib
import numpy as np
from PIL import Image

def denormalize(palette):
    return [  
        tuple(int(channel * 255) for channel in color)
        for color in palette
    ]

#Take len(data) x len(data) array 
def get_min(data):
    min_value = 2 ** 63
    for row in data:
        min_row = min(row)
        if (min_row < min_value):
            min_value = min_row

    return min_value

def get_max(data):
    max_value = -(2 ** 62)
    for row in data:
        max_row = max(row)
        if (max_row > max_value):
            max_value = max_row

    return max_value


# Alter range of values
#T: d in data: dMin <= d <= dMax
# ---->
# d' in newData: range[0] <= d' <= range[1] 
def transform(data: list, range:tuple):
    dMin = get_min(data)
    dMax = get_max(data)
    range_d = dMax - dMin
    range_c = range[1] - range[0]
    slope = float(range_c / range_d)
    newData = []
    for row in data:
        newRow = []
        for value in row:
            newRow.append(int(slope*value - slope*dMin + range[0]))
        newData.append(newRow)
    
    return newData

#Change the dimensions of data to max specified dimensions
#T: (len(data) x len(data)) -> (dim x dim)
def stretch_compress(data:list, dim:int):
    ratio = len(data) / dim
    newData = []
    for i in range(0, dim):
        row = []
        for j in range(0, dim):
            row.append(data[int(ratio*i)][int(ratio*j)])
        newData.append(row)
    assert(len(newData) == dim)
    assert(len(newData[0]) == dim)

    return newData

def ex_R3toR1(data):
    for row in data:
        for i in range(0, len(row)):
            row[i] = row[i][0] ** 2 + row[i][1] 

    return data



    

def color_image(data, map, dim, cMin=None, cMax=None, func=None):
    #print(data)
    if func != None:
        data = func(data)
    assert(type(data) == list)
    assert(type(data[0]) == list)
    assert(type(data[0][0]) != list)
    if cMin == None:
        cMin = 0
    if cMax == None:
        cMax = len(map) - 1
    data = transform(data, (cMin, cMax))
    data = stretch_compress(data, dim)
    #Format the pixels
    pixels = []
    for i in range(dim):
        row = []
        for j in range(dim):
            row.append(tuple(colormap[data[i][j] % len(colormap)]))
        pixels.append(row)
    assert(len(pixels) == dim)
    assert(len(pixels[0]) == dim)
    array = np.array(pixels, dtype=np.uint8)
    new_image = Image.fromarray(array)
    return new_image


colormap = matplotlib.cm.get_cmap("twilight_shifted").colors
colormap=denormalize(colormap)
print(len(colormap))
#exit()
data = []
for i in range(10, 500):
    row = []
    for j in range(10, 500):
        row.append(i*j)
    data.append(row)
color_image(data, colormap, 100, 100, 200).show()
exit()
data = []
for i in range(20):
    row = []
    for j in range(20):
        row.append([i,j])
    data.append(row)
print(data)
color_image(data, colormap, 100, 100, 400, func=ex_R3toR1).show()

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