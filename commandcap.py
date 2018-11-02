# encoding: utf-8

import ctypes
from ctypes.wintypes import RECT
import datetime
import os
import random
from time import sleep

from PIL import ImageGrab

def ____win32api_wrapper____():
    pass

def get_foreground_window():
    return ctypes.windll.user32.GetForegroundWindow()

def get_window_rect(hwnd):
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    ret = {
        'x1'  : rect.left,
        'y1'  : rect.top,
        'x2'  : rect.right,
        'y2'  : rect.bottom
    }
    return ret

def get_foreground_rect():
    return get_window_rect(get_foreground_window())

def get_cursor_pos():
    point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    ret = (point.x, point.y)
    return ret

def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def ____capturing____():
    pass

def capture_fullscreen():
    return ImageGrab.grab()

def capture_rect(x1, y1, x2, y2):
    return ImageGrab.grab(bbox=(x1, y1, x2, y2))

def capture_activewindow():
    hwnd = get_foreground_window()
    rect = get_window_rect(hwnd)
    return capture_rect(rect['x1'], rect['y1'], rect['x2'], rect['y2'])

def save_to_png(grab_obj, filename):
    grab_obj.save('{}.png'.format(filename))

def save_to_jpeg(grab_obj, filename):
    grab_obj.save(
        '{}.jpg'.format(filename),
        quality=100,
        optimize=True,
        progressive=True
    )

def ____funcs____():
    pass

def get_today_datetimeobj():
    return datetime.datetime.now()

def cursorshake(count, distance):
    def get_random_number_0_to_n(n):
        return random.randint(0, n)

    def shake_mousecursor(count, distance):
        mx, my = get_cursor_pos()
        for i in range(count):
            dirs = [
                [-1, -1],
                [0, -1],
                [1, -1],
                [1, 0],
                [1, 1],
                [0, 1],
                [-1, 1],
                [-1, 0],
            ]
            dirs_len = len(dirs)
            dir = dirs[get_random_number_0_to_n(dirs_len-1)]
            dx, dy = dir
            dx, dy = dx*distance, dy*distance

            set_cursor_pos(mx+dx, my+dy)
            sleep(0.015)
            set_cursor_pos(mx-dx, my-dy)
            sleep(0.005)

        set_cursor_pos(mx, my)

    shake_mousecursor(count ,distance)

def ____arguments____():
    pass

def parse_arguments(defaults):
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Simple light commandline screen capture tool.',
    )

    parser.add_argument('-f', '--fullscreen', default=False, action='store_true')
    parser.add_argument('-a', '--activewindow', default=False, action='store_true')
    parser.add_argument('-r', '--rect', default=defaults['capture']['rect_range'],
        help='Must be given with `top,left,right,bottom` by pixel.')

    parser.add_argument('-j', '--jpeg', default=True, action='store_true',
        help='Generate the image with JPEG.')
    parser.add_argument('-p', '--png', default=False, action='store_true',
        help='Generate the image with PNG. This option disable to --jpeg.')

    parser.add_argument('-o', '--output-directory', default=defaults['program']['dir'],
        help='An output directory of captured image.')
    parser.add_argument('--format', default=defaults['format']['filename'],
        help='A filename format. You can use slot1 as `$1` and slot2 as `$2`')
    parser.add_argument('--format1', default=defaults['format']['1'],
        help='A format placeholder of today datetime string based on strftime. slot1.')
    parser.add_argument('--format2', default=defaults['format']['2'],
        help='A format placeholder of today datetime string based on strftime. slot2.')

    parser.add_argument('-w', '--wait', default=0, type=int,
        help='Do sleep before capturing.')

    parser.add_argument('--disable-cursorshake', default=False, action='store_true',
        help='Disable the cursor-shake for notifying success of capturing.')
    parser.add_argument('--cursorshake-count', default=defaults['cursorshake']['count'], type=int,
        help='cursor-shake parameter: A count of shaking.')
    parser.add_argument('--cursorshake-distance', default=defaults['cursorshake']['distance'], type=int,
        help='cursor-shake parameter: A distance of mouse cursor moving when shaking.')

    parser.add_argument('-t', '--test', default=False, action='store_true',
        help='Show output filename only. (not saving image.)')

    parsed_args = parser.parse_args()
    return parsed_args

def rect_argument_to_tuple(rect_option_value):
    # a b c d => (a, b, c, d)
    ls_str = rect_option_value.split(',')
    if len(ls_str)!=4:
        raise RuntimeError('Invalid --rect format: Must be 4 elements!')
    ls_int = [int(elm) for elm in ls_str]
    return (ls_int[0], ls_int[1], ls_int[2], ls_int[3])

def ____main____():
    pass

MYFULLPATH = os.path.abspath(__file__)
MYDIR = os.path.dirname(MYFULLPATH)

formatslot1    = '%Y/%m/%d %H:%M:%S'
formatslot2    = '%y%m%d_%H%M%S'
formatfilename = '$2'
defaults = {
    'program' : {
        'fullpath'  : MYFULLPATH,
        'dir'       : MYDIR,
    },
    'format' : {
        'filename' : formatfilename,
        '1'        : formatslot1,
        '2'        : formatslot2,
    },
    'capture' : {
        'rect_range' : '0,0,100,100',
    },
    'cursorshake' : {
        'count'     : 10,
        'distance'  : 10,
    },
}

args = parse_arguments(defaults)

today_datetimeobj = get_today_datetimeobj()
slot1_str = today_datetimeobj.strftime(args.format1)
slot2_str = today_datetimeobj.strftime(args.format2)
out_basename  = args.format.replace('$1', slot1_str).replace('$2', slot2_str)
out_directory = args.output_directory
out_filefull  = os.path.join(out_directory, out_basename)

use_jpeg  = args.jpeg
use_png   = args.png
out_mode  = None
save_func = None
if use_png:
    out_mode  = 'PNG'
    save_func = save_to_png
elif use_jpeg:
    out_mode = 'JPEG'
    save_func = save_to_jpeg
else:
    raise RuntimeError('Invalid: neigher PNG or JPEG!')

use_fullcapture    = args.fullscreen
use_activecapture  = args.activewindow
use_rectcapture    = True
rect_capture_range = rect_argument_to_tuple(args.rect)
capture_func       = None
capture_args       = []
capture_mode       = None
if use_fullcapture:
    capture_func = capture_fullscreen
    capture_mode = 'Full Screen'
elif use_activecapture:
    capture_func = capture_activewindow
    capture_mode = 'Active Window'
elif use_rectcapture:
    capture_func = capture_rect
    capture_args = rect_capture_range
    capture_mode = 'Rectangle Range'

if args.test:
    print('[Output]')
    print('mode: {}'.format(out_mode))
    print('name: {}'.format(out_basename))
    print('dir : {}'.format(out_directory))
    print('full: {}'.format(out_filefull))
    print('')
    print('[Formatting]')
    print('slot1  : {} => {}'.format(args.format1, slot1_str))
    print('slot2  : {} => {}'.format(args.format2, slot2_str))
    print('format : {} => {}'.format(args.format, out_basename))
    print('')
    print('[Capture Settings]')
    print('mode: {}'.format(capture_mode))
    if capture_func==capture_rect:
        r = capture_args
        print('range: ({},{}) to ({}, {})'.format(r[0], r[1], r[2], r[3]))
    
    exit(0)

sleep(args.wait)
captured_grab = capture_func(*capture_args)
if not args.disable_cursorshake:
    cursorshake(args.cursorshake_count, args.cursorshake_distance)
save_func(captured_grab, out_filefull)
print('saved.')
