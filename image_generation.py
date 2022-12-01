import fractals as fracts
from PIL import Image
import multiprocessing as mp
from mandelbrot import MandelbrotSet
from viewport import Viewport
import os
def proxy_viewport(center=-0.7435 + 0.1314j, width=0.002, max_iterations=256, escape_count=1000, dimension=256):
    image = Image.new(mode="L", size=(dimension, dimension))
    viewport = Viewport(image, center=center, width=width)
    return viewport
    
def generate_image(center=-0.7435 + 0.1314j, width=0.002, max_iterations=256, escape_count=1000, dimension=256):
    mandelbrot_set = MandelbrotSet(max_iterations=256, escape_radius=1000)

    image = Image.new(mode="L", size=(dimension, dimension))
    viewport = Viewport(image, center=center, width=width)
    for pixel in viewport:
        c = complex(pixel)
        instability = 1 - mandelbrot_set.stability(c, smooth=True)
        pixel.color = int(instability * 255)

    image.save(os.path.join("assets", "image") + ".jpg")
    return viewport

if __name__ == '__main__':
    generate_image(center = -1, width = 2)
