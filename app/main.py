import numpy as np
from PIL import ImageGrab, Image
import cv2
from directKeys import query_key_state, move_window, KEY_Q, KEY_CONTROL
import time
import math
import autoit

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

def is_white(c):
    r = int(c[0])
    g = int(c[1])
    b = int(c[2])
    if r > 75 and g > 75 and b > 75 and abs(r - g) < 10 and abs(r - b) < 10:
        return True;
    return False

def is_blob_white(x, y):
    for xi in range(x, x + 3):
        for yi in range(y, y + 3):
            c = get_color(xi, yi)
            if not is_white(c):
                return False
    return True

def is_brighter(p1, p2):
    c1 = get_color(p1[0], p1[1])
    c2 = get_color(p2[0], p2[1])
    if c1[0] > c2[0]:
        return True
    return False

def find_bobber_pos():
    possible_positions = []
    for x in range(75, 330):
        for y in range(380, 620):
            c = get_color(x, y)
            if is_white(c) and is_blob_white(x, y):
                possible_positions.append([x, y])
           
    if len(possible_positions) > 0:
        best = possible_positions[0]
        for p in possible_positions:
            if is_brighter(p, best):
                best = p
        return best
    
    return None
            

# only start the program after the mouse is in the top left corner
print("move the mouse to the upper left corner to start")
while True:
    mouse_pos = autoit.mouse_get_pos()
    if mouse_pos[0] <= 0 and mouse_pos[1] <= 0:
        break

print("here we go")
move_window(u'WINDOWSCLIENT', None, 0, 0, 1000, 800)
text_color = None
bobber_pos = None
while not query_key_state(KEY_CONTROL):
    print("checking (hold CTRL to exit)")
    read_screen()
    
    if text_color is None:
        text_color = get_color(476, 771)
        print(f"text_color found {text_color}")
    
    c = get_color(482, 779)
    is_cast = check_color(482, 779, text_color)
    is_pull = check_color(513, 764, text_color)
    print(f"is_cast {is_cast}")
    print(f"is_pull {is_pull}")
    
    if is_cast:
        bobber_pos = None
        autoit.mouse_click("left", 500, 732)
        time.sleep(1)
        
    if is_pull:
        if bobber_pos is None:
            print(f"find bobber")
            bobber_pos = find_bobber_pos()
        else:
            print(f"check bobber")
            c = get_color(bobber_pos[0], bobber_pos[1])
            if not is_white(c):
                print(f"found fish")
                bobber_pos = None
                autoit.mouse_click("left", 500, 732)
                time.sleep(1)
        
    autoit.mouse_move(0, 0)
   
print("done")
