from Xlib import display, X
from PIL import Image, ImageOps
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

ZUMA_WIDTH = 642
ZUMA_HEIGHT = 514

def take_screenshot(x, y, h, w):
    dsp = display.Display()
    dir(dsp.screen())
    root = dsp.screen().root
    raw = root.get_image(x, y, w, h, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (w, h), raw.data, "raw", "BGRX")
    return image


def get_score(image):
    score_zone = ImageOps.invert(image.crop((275, 1, 365, 20)))
    ocr_result = pytesseract.image_to_string(score_zone,
                                         config=f'--psm 7 -c tessedit_char_whitelist=0123456789')
    return int(ocr_result)


def get_zuma_geometry(dsp):
    root = dsp.screen().root
    children = root.query_tree().children

    for window in children:
        geometry = window.get_geometry()._data
        if abs(geometry["width"] - ZUMA_WIDTH) < 5 and abs(geometry["height"] - ZUMA_HEIGHT) < 5:
            print("FOUND")
            return (geometry["x"],
                    geometry["y"]+33,
                    geometry["height"]-33,
                    geometry["width"])
    return None


def map_coords_to_screen(x, y, geometry):
    x = min(max(x, 0), geometry[3])
    y = min(max(y, 0), geometry[2])
    return x + geometry[0], y + geometry[1]


dsp = display.Display()

geometry = get_zuma_geometry(dsp)


image = take_screenshot(*geometry)

score = get_score(image)


print(score)

import mouse_controle

mouse_controle.set_mouse_position(*map_coords_to_screen(200, 30, geometry))
mouse_controle.click()