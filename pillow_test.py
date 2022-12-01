import fractals as fracts
from PIL import Image
import multiprocessing as mp
from mandelbrot import MandelbrotSet
from viewport import Viewport
import os
# c = fracts.complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=512)
# image = Image.fromarray(~fracts.is_stable(c, num_iterations=20))
# image.show()

def image(width, height, iterations):
    scale = .0075 * (512 / width)
    image = Image.new(mode='L', size=(width, height))
    for y in range(height):
        for x in range(width):
            c = scale * complex(x - width / 2, height / 2 - y)
            instability = 1 - fracts.stability(c, iterations)
            image.putpixel((x, y), int(instability * 255))

    image.show()


#image(1024, 1024, 10)


mandelbrot_set = MandelbrotSet(max_iterations=256, escape_radius=1000)

image = Image.new(mode="L", size=(1024, 1024))
for pixel in Viewport(image, center=-0.7435 + 0.1314j, width=0.002):
    c = complex(pixel)
    instability = 1 - mandelbrot_set.stability(c, smooth=True)
    pixel.color = int(instability * 255)

image.save(os.path.join("assets", "image") + ".jpg")

# # scale = .0075 / 2
# # width, height = 1024, 1024
# # image = Image.new(mode='L', size=(width, height))
# # for y in range(height):
# #     for x in range(width):
# #         c = scale * complex(x - width / 2, height / 2 - y)
# #         instability = 1 - fracts.stability(c, 20)
# #         image.putpixel((x, y), int(instability * 255))

# # image.show()

# def par_callback(image, height, width, scale, x):
#     for y in height:
#         c = scale * complex(x - width / 2, height / 2 - y)
#         instability = 1 - fracts.stability(c, 20)
#         image.putpixel((x, y), int(instability * 255))

    

# def image_par(width, height):
#     scale = .0075 * (512 / width)
#     image = Image.new(mode='L', size=(width, height))
#     pool = mp.Pool(mp.cpu_count())
#     #results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
#     [pool.apply(par_callback, args=(image, height, scale, x))  for x in range(width)]
#     pool.close()
#     image.show()


# width, height = 512, 512
# scale = .0075 * (512 / width)
# image = Image.new(mode='L', size=(width, height))
# pool = mp.Pool(mp.cpu_count())
# #results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
# [pool.apply(par_callback, args=(image, height, width, scale, x))  for x in range(width)]
# pool.close()
# image.show()

