import numpy as np
from PIL import Image, ImageFilter
from formulas_parsing import parse_formulas
from function_generation import generate_graph_fun, generate_vars_fun
from image_utilities import graph_to_image, draw_coords


class GraphDrawer:
    def __init__(self, img_w: int = 1000, img_h: int = 1000,
                 units_per_pixel: float = 0.1, c_x: float = 0, c_y: float = 0,
                 frames: int = 1):
        self.img_w = img_w
        self.img_h = img_h
        self.units_per_pixel = units_per_pixel
        self.c_x = c_x
        self.c_y = c_y
        self.frames = frames
        self.field = self.generate_field()

    def generate_field(self):
        lst = np.indices((self.img_h, self.img_w), dtype='double')

        lst[1] = self.ind_to_x(lst[1])
        lst[0] = self.ind_to_y(lst[0])

        field = np.dstack((lst[1], lst[0]))
        return field

    def ind_to_x(self, i):
        return (i - self.img_w / 2) * self.units_per_pixel + self.c_x

    def ind_to_y(self, i):
        return - (i - self.img_h / 2) * self.units_per_pixel + self.c_y

    def calculate_graphs(self, text):
        formulas, cases, variables = parse_formulas(text)

        var_fun = generate_vars_fun(variables)
        var_array = np.zeros((len(variables), self.img_h, self.img_w,))

        var_fun = np.vectorize(var_fun)
        var_array[...] = var_fun(self.field[..., 0], self.field[..., 1])

        graph_fun = generate_graph_fun(formulas, variables)
        graph_array = np.zeros((len(formulas), self.img_h, self.img_w,))

        graph_fun = np.vectorize(graph_fun)
        graph_array[...] = graph_fun(self.field[..., 0], self.field[..., 1],
                                     *(e[:] for e in var_array))

        return graph_array, cases

    def draw(self, text: str, colors,  filename: str):
        from time import time

        start = time()
        graph_array, cases = self.calculate_graphs(text)

        color_i = 0
        res = draw_coords(self.img_w, self.img_h, self.units_per_pixel, self.c_x, self.c_y)
        for graph, mode in zip(graph_array, cases):
            color = colors[color_i]
            color_i = (color_i + 1) % len(colors)

            im = graph_to_image(graph, mode, color)
            res = Image.alpha_composite(res, im)

        res.save(filename)
        end = time()
        print(end-start)




if __name__ == '__main__':
    a = GraphDrawer(img_w=1000, img_h=1000, units_per_pixel=0.005)
    colors = (
        (125, 125, 255),
        (0, 0, 0),
        (0, 0, 0)
    )
    a.draw('sin(x^3 * y^2) = cos(x^2 * y^3)', colors,  '1213.png')
