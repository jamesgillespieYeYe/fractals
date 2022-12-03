import fractals as fracts
from PIL import Image
import multiprocessing as mp
from mandelbrot import MandelbrotSet
from viewport import Viewport
import os
import matplotlib.cm
def proxy_viewport(center=-0.7435 + 0.1314j, width=0.002, max_iterations=256, escape_count=1000, dimension=256):
    image = Image.new(mode="L", size=(dimension, dimension))
    viewport = Viewport(image, center=center, width=width)
    return viewport

def denormalize(palette):
    return [  
        tuple(int(channel * 255) for channel in color)
        for color in palette
    ]

def paint(mandelbrot_set, viewport, palette, smooth):
    #print("palette: ", palette)
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        index = int(min(stability * len(palette), len(palette) - 1))
        #print("index: ", stability * len(palette))
        #print(palette[index % len(palette)])
        pixel.color = palette[index % len(palette)]
    
def generate_image(center=-0.7435 + 0.1314j, width=0.002, max_iterations=256, escape_count=1000, dimension=256, colormap=False, map='twilight'):
    mandelbrot_set = MandelbrotSet(max_iterations=256, escape_radius=1000)
    if not colormap:
        image = Image.new(mode="L", size=(dimension, dimension))
    else:
        image = Image.new(mode="RGB", size=(dimension, dimension))
    viewport = Viewport(image, center=center, width=width)
    center_pixel = None
    if not colormap:
        for pixel in viewport:
            c = complex(pixel)
            #if (abs(c - center) < .1):
                #print("Found center!")
                #pixel.color = 255
            #else:
                #instability = 1 - mandelbrot_set.stability(c, smooth=True)
                #pixel.color = int(instability * 255)
            instability = 1 - mandelbrot_set.stability(c, smooth=True)
            pixel.color = int((1 - instability) * 255 + 15)
    else:
        colormap = matplotlib.cm.get_cmap(map).colors
        palette = denormalize(colormap)
        paint(mandelbrot_set, viewport, palette, smooth=False)

        

    image.save(os.path.join("assets", "image") + ".jpg")
    return viewport

if __name__ == '__main__':
    generate_image(center = -1, width = 2)
