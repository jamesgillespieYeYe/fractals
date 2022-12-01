from dataclasses import dataclass
from PIL import Image
import json


@dataclass
class Viewport:
    image: Image.Image
    center: complex
    width: float

    @property
    def height(self):
        return self.scale * self.image.height

    @property
    def offset(self):
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self):
        return self.width / self.image.width

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)
@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.getpixel((self.x, self.y))

    @color.setter
    def color(self, value):
        self.viewport.image.putpixel((self.x, self.y), value)

    def __complex__(self):
        return (
                complex(self.x, -self.y)
                * self.viewport.scale
                + self.viewport.offset
        )

class ViewportData:
    center_re: float
    center_im: float
    width: float
    image_height: int
    image_width: int

    def __init__(self, viewport:Viewport):
        self.center_re = viewport.center.real
        self.center_im = viewport.center.imag
        self.width = viewport.width
        self.image_height = viewport.image.height
        self.image_width = viewport.image.width


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)