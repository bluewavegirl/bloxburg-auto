import numpy as np
from PIL import ImageGrab, Image
import cv2
from directKeys import click, move_mouse_to, query_mouse_position, press_key, release_key, query_key_state, move_window, KEY_Q, KEY_CONTROL
import time
import math

game_coords = [0, 0, 1000, 800]

debug_tracking = True

screen = None

def read_screen():
    global screen
    screen = np.array(ImageGrab.grab(bbox=game_coords))
    # screen = np.array(Image.open('C:/dev/grow-tower-auto-clicker-files/where-is-the-diamond-02.png'))
    return screen

def get_color(x, y):
    return screen[y, x]

def check_color(x, y, color):
    return np.array_equal(get_color(x, y), color)

def check_color_around(x, y, radius, color):
    for ix in range(x - radius, x + radius):
        for iy in range(y - radius, y + radius):
            if check_color(ix, iy, color):
                return True
    return False

# only start the program after the mouse is in the top left corner
print("move the mouse to the upper left corner to start")
while True:
    mouse_pos = query_mouse_position()
    if mouse_pos.x <= 0 and mouse_pos.y <= 0:
        break

print("here we go")
move_window(u'WINDOWSCLIENT', None, 0, 0, 1000, 800)
while not query_key_state(KEY_CONTROL):
    print("checking (hold CTRL to exit)")
    read_screen()
    
    
    time.sleep(1)
    move_mouse_to(100, 100)
    time.sleep(1)
    move_mouse_to(200, 200)

print("done")
