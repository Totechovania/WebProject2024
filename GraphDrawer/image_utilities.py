import numpy as np
from PIL import Image, ImageFilter


def make_transparent_and_colorful(img: Image, graph_color,):
    img = img.convert(mode='RGBA')
    data = np.array(img)

    black_areas = (data[..., 0] == 0) & (data[..., 1] == 0) & (data[..., 2] == 0)

    data[...] = graph_color
    data[...][black_areas] = (0, 0, 0, 0)

    return data

def line_from_array(array):
    im = Image.fromarray(array)
    im = im.filter(ImageFilter.FIND_EDGES)
    return im


def graph_to_image(graph: np.array, mode: str, color: np.array):
    not_defined = np.isnan(graph)
    graph[not_defined] = 0
    graph = sign(graph[:])

    marking_colors = np.array([(255, 255, 255), (255, 0, 0), (0, 0, 255)], dtype='uint8')
    graph = marking_colors[graph]

    img = line_from_array(graph)
    data = make_transparent_and_colorful(img, color)

    data[not_defined] = (0, 0, 0, 0)
    img = Image.fromarray(data)

    return img



@np.vectorize
def sign(i):
    if i == 0:
        return 0
    elif i > 0:
        return 1
    elif i < 0:
        return 2
