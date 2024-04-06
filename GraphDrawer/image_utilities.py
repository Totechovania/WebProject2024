import numpy as np
from PIL import Image, ImageFilter


def make_transparent_and_colorful(data: np.array, graph_color,):
    if len(graph_color) == 3:
        graph_color = (*graph_color, 255)

    h, w = data.shape[:2]
    data = np.concatenate((data, np.zeros((h, w, 1), dtype='uint8'),), axis=2)

    black_areas = (data[..., 0] == 0) & (data[..., 1] == 0) & (data[..., 2] == 0)

    data[...] = graph_color
    data[...][black_areas] = (0, 0, 0, 0)

    return data


def line_from_array(data: np.array):
    im = Image.fromarray(data)
    im = im.filter(ImageFilter.FIND_EDGES)
    data = np.array(im)
    return data


def figure_from_array(data: np.array, mark_color):
    to_cut = (data[..., 0] != mark_color[0]) | (data[..., 1] != mark_color[1]) | (data[..., 2] != mark_color[2])
    data[...][to_cut] = (0, 0, 0)
    return data


def graph_to_image(data: np.array, mode: str, color: tuple):
    not_defined = np.isnan(data)
    data[not_defined] = 0
    data = sign(data[:])

    marking_colors = np.array([(255, 255, 255), (255, 0, 0), (0, 0, 255)], dtype='uint8')
    data = marking_colors[data]

    if mode == '=':
        data = line_from_array(data)
        data = make_transparent_and_colorful(data, color)
    elif mode == '>':
        data = figure_from_array(data, marking_colors[1])
        data = make_transparent_and_colorful(data, (*color[:3], 125))
    elif mode == '>=':
        line_data = data
        figure_data = np.copy(data)

        line_data = line_from_array(line_data)
        line_data = make_transparent_and_colorful(line_data, color)

        figure_data = figure_from_array(figure_data, marking_colors[1])
        figure_data = make_transparent_and_colorful(figure_data, (*color[:3], 125))

        data = np.where(line_data[...] != (0, 0, 0, 0), line_data, figure_data)

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
