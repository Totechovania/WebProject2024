import base64
from io import BytesIO

from PIL import Image


def avatar_to_bytes(img_raw):
    image_file = BytesIO()
    img_raw = img_raw.split(",")[1]
    img = Image.open(BytesIO(base64.b64decode(img_raw)))
    img = img.resize((400, 400))
    img.save(image_file, format='png')
    imagedata = image_file.getvalue()
    return base64.b64encode(imagedata)
