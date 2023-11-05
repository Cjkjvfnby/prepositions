import base64
from io import BytesIO
from pathlib import Path
from typing import TypeAlias

from PIL import Image, ImageFont

_FONT_PATH = (
    Path(__file__).parent / "static" / "Roboto" / "Roboto-Regular.ttf"
).as_posix()


Color: TypeAlias = tuple[int, int, int, int] | tuple[int, int, int]


def add_margin(
    pil_img: Image,
    *,
    horizontal: int,
    vertical: int,
    color: Color,
) -> Image:
    width, height = pil_img.size
    new_width = width + 2 * horizontal
    new_height = height + 2 * vertical
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (horizontal, vertical))
    return result


def icon_from_text(text: str, color: Color) -> str:
    """
    Return icon as HTML img src.
    """
    font_size = 72

    font = ImageFont.truetype(_FONT_PATH, size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGBA", mask_image.size, (255, 0, 0, 0))
    img.im.paste(
        color,
        (0, 0, *mask_image.size),
        mask_image,
    )  # need to use the inner `img.im.paste` due to `getmask` returning a core

    img = add_margin(img, horizontal=60, vertical=60, color=(255, 0, 0, 0))

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")

    image_base64 = base64.encodebytes(img_byte_arr.getvalue()).decode()
    return f"data:image/png;base64,{image_base64}"
