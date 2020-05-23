from pynput.mouse import Button, Controller

mouse = Controller()


def get_mouse_position():
    return mouse.position


def click():
    mouse.click(Button.left)


def set_mouse_position(x, y):
    mouse.position = (x, y)
