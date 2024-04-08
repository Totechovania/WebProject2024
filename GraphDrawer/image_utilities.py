import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def make_transparent_and_colorful(data: np.array, graph_color,):
    if len(graph_color) == 3:
        graph_color = (*graph_color, 215)

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


def draw_coords(img_w: int = 1000, img_h: int = 1000, units_per_pixel: float = 0.1, c_x: float = 0, c_y: float = 0,):
    img = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    step = beautiful_round(img_w * units_per_pixel / 10)

    l_x = c_x - img_w * units_per_pixel / 2
    r_x = c_x + img_w * units_per_pixel / 2
    x_text_draw = []

    u_y = c_y + img_h * units_per_pixel / 2
    d_y = c_y - img_h * units_per_pixel / 2
    y_text_draw = []

    cur_x = l_x // step * step

    while cur_x <= r_x:
        x_ind = (cur_x - c_x + (r_x - l_x) / 2) / units_per_pixel
        draw.line((x_ind, 0, x_ind, img_h), fill=(225, 225, 225, 255), width=1)
        cur_x += step / 4

    cur_y = d_y // step * step
    while cur_y <= u_y:
        y_ind = -(cur_y - c_y - (u_y - d_y) / 2) / units_per_pixel
        draw.line((0, y_ind, img_w, y_ind), fill=(225, 225, 225, 255), width=1)
        cur_y += step / 4

    cur_x = l_x // step * step
    while cur_x <= r_x:
        x_ind = (cur_x - c_x + (r_x - l_x) / 2) / units_per_pixel
        draw.line((x_ind, 0, x_ind, img_h), fill=(125, 125, 125, 255), width=1)
        x_text_draw.append((cur_x, x_ind))
        cur_x += step

    cur_y = d_y // step * step
    while cur_y <= u_y:
        y_ind = -(cur_y - c_y - (u_y - d_y) / 2) / units_per_pixel
        draw.line((0, y_ind, img_w, y_ind), fill=(125, 125, 125, 255), width=1)
        y_text_draw.append((cur_y, y_ind))
        cur_y += step

    font = draw.getfont()
    font.size = 100
    x_ind = (-c_x + (r_x - l_x) / 2) / units_per_pixel
    y_ind = -(-c_y - (u_y - d_y) / 2) / units_per_pixel

    y_axis_visible = l_x <= 0 <= r_x
    x_axis_visible = d_y <= 0 <= u_y
    if x_axis_visible:
        draw.line((0, y_ind, img_w, y_ind), fill=(0, 0, 0, 255), width=2)
        for text, pos in x_text_draw:
            draw.text((pos, y_ind), str(text), fill=(0, 0, 0, 255), font=font, anchor='ra')

    if y_axis_visible:
        draw.line((x_ind, 0, x_ind, img_h), fill=(0, 0, 0, 255), width=2)
        for text, pos in y_text_draw:
            draw.text((x_ind, pos), str(text), fill=(0, 0, 0, 255), font=font, anchor='ra')

    return img


def beautiful_round(n):
    num, e = f'{n:.2e}'.split('e')
    num = round(float(num))
    e = int(e)
    if num == 1:
        num = 1
    elif 2 <= num <= 3:
        num = 2
    elif 4 <= num <= 6:
        num = 5
    elif 7 <= num <= 10:
        num = 1
        e += 1
    return num * 10 ** e


draw_coords().save('coords.png')