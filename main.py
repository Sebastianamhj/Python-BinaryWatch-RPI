from sense_hat import SenseHat
from datetime import datetime
import time
import numpy
from sense_hat.stick import ACTION_RELEASED
import signal
import sys

display_mode = 1
time_mode = True

"""
def getBackground():
    global time_mode
    value = datetime.now().hour
    if time_mode == False:
        if value >= 12: return (255,255,255); return (0,0,255)
    else:
        return (0,0,255)
"""
# Colors for LED
hour_color = (255, 0, 255)
minute_color = (0, 255, 128)
second_color = (255, 128, 0)

sense = SenseHat()

sense.clear()


def main():
    starting()
    BinaryClock()


def starting():
    sense.show_message("Starting soon", 0.1, minute_color, (0, 0, 185))
    sense.clear()


def draw(value, row, color):
    binary_str = "{0:8b}".format(value)
    for x in range(0, 8):
        if binary_str[x] == '1':
            sense.set_pixel(x, row, color)
        else:
            sense.set_pixel(x, row, 0, 0, 0)


"""
def drawTwo(value, row, color):
    length = len(str(value))
    if length > 1:
        binary_ones = "{0:8b}".format(int(str(value)[1]))
        binary_tens = "{0:8b}".format(int(str(value)[0]))
        for x in range(0,8):
            if binary_ones[x] == '1':
                sense.set_pixel(x, row, color)
            else:
                sense.set_pixel(x, row, off)
            if binary_tens[x] == '1':
                sense.set_pixel(x, row +1, color)
            else:
                sense.set_pixel(x, row +1, off)
    else:
        binary_ones = "{0:8b}".format(value)    
        for x in range(0,8):
            if binary_ones[x] == '1':
                sense.set_pixel(x, row, color)
            else:
                sense.set_pixel(x, row, off)  

def OptionTwo():
    global display_mode

    while display_mode == 0:
        t = datetime.datetime.now()
        drawTwo(t.hour, 1, hour_color)
        drawTwo(t.minute, 3, minute_color)
        drawTwo(t.second, 5, second_color)
        time.sleep(0.9)
"""


def BinaryClock():
    global display_mode
    global time_mode
    global hour_color

    while True:
        t = datetime.now()
        if (time_mode):
            h = int(t.strftime('%H'))
            m = int(t.strftime('%M'))
            s = int(t.strftime('%S'))
        else:
            h = int(t.strftime('%I'))
            m = int(t.strftime('%M'))
            s = int(t.strftime('%S'))

        if display_mode == 1:
            sense.set_rotation(0)
            draw(h, 3, hour_color)
            draw(m, 4, minute_color)
            draw(s, 5, second_color)
        elif display_mode == 2:
            sense.set_rotation(90)
            draw(h % 10, 1, hour_color)
            draw(h // 10, 2, hour_color)
            draw(m % 10, 3, minute_color)
            draw(m // 10, 4, minute_color)
            draw(s % 10, 5, second_color)
            draw(s // 10, 6, second_color)

        time.sleep(0.9)


def pushed_up(event):
    global time_mode
    if event.action != ACTION_RELEASED:
        print("up")
        time_mode = not time_mode
        sense.clear()


def pushed_down(event):
    if event.action != ACTION_RELEASED:
        print("down")
        sense.set_rotation(0)


def pushed_left(event):
    global display_mode
    if event.action != ACTION_RELEASED:
        print("left")
        display_mode = 1


def pushed_right(event):
    global display_mode
    if event.action != ACTION_RELEASED:
        print("right")
        display_mode = 2


def refresh():
    sense.clear()
    pass


def signal_handler(sig, frame):
    print('You pressed ctrl+c!')
    sense.set_rotation(0)
    sense.show_message("Shutting down", 0.1, minute_color, (0, 0, 185))
    sense.clear()
    sys.exit(0)


sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_any = refresh

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
main()
