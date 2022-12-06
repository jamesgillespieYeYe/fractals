# mandelbrot.py

from dataclasses import dataclass
from math import log

@dataclass
class JuliaSet:
    max_iterations: int
    parameter: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False):
        z = c
        print(z)
        for iteration in range(self.max_iterations):
            z = z ** 2 + self.parameter
            #print(z)
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
        return self.max_iterations