import base64
import os
import tempfile

import six
import torch
from PIL import Image
from flask import Flask, request
from flask import jsonify

import process_stylization
from image_utils import base64_png_image_to_pillow_image, get_apt_image_size, get_temp_png_file_path
from photo_wct import PhotoWCT

app = Flask(__name__)

MAX_NUM_PIXELS = 1024 * 512

# Load model
p_wct = PhotoWCT()
try:
    p_wct.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), 'PhotoWCTModels', 'photo_wct.pth')))
except:
    print("Fail to load PhotoWCT models. PhotoWCT submodule not updated?")
    exit()


@app.route("/stylize/", methods=['POST'])
def stylize():
    content_image_base64 = request.json.get('content_image_base64', None)
    if content_image_base64 is None:
        raise Exception('content_image_base64 cannot be None')
    else:
        content_image = base64_png_image_to_pillow_image(content_image_base64)

    style_image_base64 = request.json.get('style_image_base64', None)
    if style_image_base64 is None:
        raise Exception('style_image_base64 cannot be None')
    else:
        style_image = base64_png_image_to_pillow_image(style_image_base64)

    content_segmentation_base64 = request.json.get('content_segmentation_base64', None)
    if content_segmentation_base64 is None:
        content_segmentation = None
    else:
        content_segmentation = base64_png_image_to_pillow_image(content_segmentation_base64)

    style_segmentation_base64 = request.json.get('style_segmentation_base64', None)
    if style_segmentation_base64 is None:
        style_segmentation = None
    else:
        style_segmentation = base64_png_image_to_pillow_image(style_segmentation_base64)

    if (content_segmentation is None) != (style_segmentation is None):
        raise Exception('Content segmentation must either be both set or both None')

    original_content_image_size = content_image.size
    content_image_size = get_apt_image_size(content_image, MAX_NUM_PIXELS)
    content_image = content_image.resize(content_image_size, Image.LANCZOS)
    if content_segmentation:
        content_segmentation = content_segmentation.resize(content_image_size, Image.LANCZOS)

    style_image_size = get_apt_image_size(style_image, MAX_NUM_PIXELS)
    style_image = style_image.resize(style_image_size, Image.LANCZOS)
    if style_segmentation:
        style_segmentation = style_segmentation.resize(style_image_size, Image.LANCZOS)

    content_image_path = get_temp_png_file_path()
    content_image.save(content_image_path)
    if content_segmentation:
        content_segmentation_path = get_temp_png_file_path()
        content_segmentation.save(content_segmentation_path)
    else:
        content_segmentation_path = None

    style_image_path = get_temp_png_file_path()
    style_image.save(style_image_path)
    if style_segmentation:
        style_segmentation_path = get_temp_png_file_path()
        style_segmentation.save(style_segmentation_path)
    else:
        style_segmentation_path = None

    output_image_path = get_temp_png_file_path()

    process_stylization.stylization(
        p_wct=p_wct,
        content_image_path=content_image_path,
        style_image_path=style_image_path,
        content_seg_path=content_segmentation_path,
        style_seg_path=style_segmentation_path,
        output_image_path=output_image_path,
        cuda=1,
    )

    output_image = Image.open(output_image_path)
    output_image = output_image.resize(original_content_image_size, Image.LANCZOS)

    image_buffer = six.BytesIO()
    output_image.save(image_buffer, format='PNG')
    output_image_base64 = base64.b64encode(image_buffer.getvalue())

    return jsonify({'output_image_base64': output_image_base64})


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=False  # debug=False avoids multiple threads
    )
