import base64
from io import BytesIO
from utilities.draw import hex_to_rgb
from GraphDrawer.GraphDrawer import GraphDrawer


def generate_graph_preview(graph_params):
    colors = graph_params['colors']
    for i in range(len(colors)):
        colors[i] = hex_to_rgb(colors[i][1:])

    drawer = GraphDrawer(int(graph_params['width']),
                         int(graph_params['height']),
                         1 / float(graph_params['pixel_per_unit']),
                         float(graph_params['center_x']),
                         float(graph_params['center_y']))

    img = drawer.draw(graph_params['formulas'], colors)

    img = img.resize((300, int(img.size[1] * 300 / img.size[0])))
    image_file = BytesIO()
    img.save(image_file, format='PNG')
    imagedata = image_file.getvalue()

    return base64.b64encode(imagedata)
