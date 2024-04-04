import numpy as np
from PIL import Image, ImageFilter


def make_transparent_and_colorful(img: Image, graph_color,):
    img = img.convert(mode='RGBA')
    data = np.array(img)

    black_areas = (data[..., 0] == 0) & (data[..., 1] == 0) & (data[..., 2] == 0)

    data[...] = graph_color
    data[...][black_areas] = (0, 0, 0, 0)

    img = Image.fromarray(data)

    return img


def graph_from_array(array):
    im = Image.fromarray(array)
    im = im.filter(ImageFilter.FIND_EDGES)
    return im
