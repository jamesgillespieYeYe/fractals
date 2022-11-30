import fractals as fracts
from PIL import Image
c = fracts.complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=512)
image = Image.fromarray(~fracts.is_stable(c, num_iterations=20))
image.show()
