import numpy as np
import matplotlib.pyplot as plt
import cmath

np.warnings.filterwarnings("ignore")
def complex_matrix(xmin, xmax, ymin, ymax, pixel_density):
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j

def is_stable(c, num_iterations):
    z = 0
    for _ in range(num_iterations):
        z = z ** 2 + c
    return abs(z) <= 2

def get_members(c, num_iterations):
    mask = is_stable(c, num_iterations)
    return c[mask]

def is_stable_julia(candidates, parameter, num_iterations):
    z = candidates
    for _ in range(num_iterations):
        z = z **2 + parameter
    return abs(z) <= 2

def get_members_julia(candidates, parameter, num_iterations):
    mask = is_stable_julia(candidates, parameter, num_iterations)
    return candidates[mask]
#--------------------------------------------------------
def sequence(c, z=0):
    z = 0
    while True:
        yield z
        z = z ** 2 + c

        
def first_n_elements(c, n, z=0):
    xList = []
    yList = []
    for x, z in enumerate(sequence(c, z)):
        xList.append(x)
        yList.append(abs(z))
        if (x == n):
            break
    return (xList, yList)
if __name__ == '__main__':

    c = complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=512)
    members = get_members(c, num_iterations=20)

    plt.scatter(members.real, members.imag, color="black", marker=",", s=1)
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
