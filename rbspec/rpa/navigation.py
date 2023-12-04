"""
# Developer: Richard Raphael Banak
# Objective: Functions to help RPA navigation using mouse and keyboard commands
# Creation date: 2022-07-15
"""

import pyautogui
from datetime import datetime

""" Keys of the keyboard:
\t, \n, \r,  , !, ", #, $, %, &, ', (,
), *, +, ,, -, ., /, 0, 1, 2, 3, 4, 5, 6, 7,
8, 9, :, ;, <, =, >, ?, @, [, \, ], ^, _, `,
a, b, c, d, e,f, g, h, i, j, k, l, m, n, o,
p, q, r, s, t, u, v, w, x, y, z, {, |, }, ~,
accept, add, alt, altleft, altright, apps, backspace,
browserback, browserfavorites, browserforward, browserhome,
browserrefresh, browsersearch, browserstop, capslock, clear,
convert, ctrl, ctrlleft, ctrlright, decimal, del, delete,
divide, down, end, enter, esc, escape, execute, f1, f10,
f11, f12, f13, f14, f15, f16, f17, f18, f19, f2, f20,
f21, f22, f23, f24, f3, f4, f5, f6, f7, f8, f9,
final, fn, hanguel, hangul, hanja, help, home, insert, junja,
kana, kanji, launchapp1, launchapp2, launchmail,
launchmediaselect, left, modechange, multiply, nexttrack,
nonconvert, num0, num1, num2, num3, num4, num5, num6,
num7, num8, num9, numlock, pagedown, pageup, pause, pgdn,
pgup, playpause, prevtrack, print, printscreen, prntscrn,
prtsc, prtscr, return, right, scrolllock, select, separator,
shift, shiftleft, shiftright, sleep, space, stop, subtract, tab,
up, volumedown, volumemute, volumeup, win, winleft, winright, yen,
command, option, optionleft, optionright
"""

# windows
def get_window_size():
    return pyautogui.size()


# mouse
def get_mouse_position(print_log=True):
    point = pyautogui.position()
    if print_log:
        print(f"nv.move_mouse_to(x={point.x}, y={point.y})\n")
    return point


def move_mouse_to(x, y, duration=0):
    pyautogui.moveTo(x=x, y=y, duration=duration)


def move_mouse_relative(x, y, duration=0):
    pyautogui.moveRel(xOffset=x, yOffset=y, duration=duration)


def click(x, y):
    pyautogui.click(x=x, y=y)


def drag_mouse_to(x=0, y=0, duration=1):
    pyautogui.dragTo(x=x, y=y, duration=duration, button="left")


def mouse_scroll(y=-1000):
    pyautogui.scroll(y)


# keyboard
def key_press_and_hold(key):
    pyautogui.keyDown(key)


def key_press_and_release(key):
    pyautogui.keyUp(key)


def type_text(text):
    pyautogui.typewrite(str(text))


def type_characters(text):
    for i in str(text):
        pyautogui.typewrite(i)


def type_List(key_list):
    # a, left, ctrlleft
    pyautogui.typewrite(key_list)


def hotkey(*args):
    # ex: args = "ctrlleft", "a"
    pyautogui.hotkey(*args)


# search elements
def get_image_position(image_path, timeout=None):
    start_time = datetime.now()
    element_exists = False

    while not element_exists:
        box = None
        try:
            box = pyautogui.locateOnScreen(image_path)
        except:
            pass

        if box != None:
            element_exists = True

        if timeout:
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= timeout:
                raise Exception(f"Timeout, image not found: {image_path}")

    # press on the middle of the image
    x = box.left + (box.width / 2)
    y = box.top + (box.height / 2)

    return x, y


def click_at_image(image_path, timeout=None):
    x, y = get_image_position(image_path=image_path, timeout=timeout)
    click(x=x, y=y)
    
    
def wait_for_image(image_path, timeout=None):
    get_image_position(image_path=image_path, timeout=timeout)
