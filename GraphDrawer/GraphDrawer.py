import numpy as np
from PIL import Image, ImageFilter
from formulas_parsing import parse_formulas
from function_generation import generate_graph_fun, generate_vars_fun


class GraphDrawer:
    def __init__(self,  img_w: int = 1000, img_h: int = 1000,
                 scale: float = 0.1, c_x: float = 0, c_y: float = 0,
                 frames: int = 1):
        self.img_w = img_w
        self.img_h = img_h
        self.scale = scale
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
        return (i - self.img_w / 2) * self.scale + self.c_x

    def ind_to_y(self, i):
        return - (i - self.img_h / 2) * self.scale + self.c_y

    def draw(self, formulas: str, filename: str):
        formulas, cases, variables = parse_formulas(formulas)
        var_fun = generate_vars_fun(variables)
        var_array = np.zeros((len(variables), self.img_h, self.img_w,))

        var_fun = np.vectorize(var_fun)
        var_array[...] = var_fun(self.field[..., 0], self.field[..., 1])
        print(var_array)
        print(var_array.shape)

        graph_fun = generate_graph_fun(formulas, variables)


a = GraphDrawer()

a.draw('d=x ** y\nk=0\ny=x\nsin(x)=cos(y)', '1213')




