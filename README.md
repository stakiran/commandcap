# commandcap
Simple light commandline screen capture tool for Windows.

## Feature
- Quick capture from command-line.
- Three capture mode.
  - Active Window
  - Full Screen
  - Rectangle
- Flexible output-filename format.
- Cursor shaking to notifying success of capturing.

## Requirement
- Windows 7+
- Python 3.6+
- PIL
  - Do `pip install pillow`.

## Samples

### Wrapper batch
There are many samples.

- cap_activewindow_after_3sec.bat
- cap_fullscreen_with_png.bat
- cap_rect_cursorshake_big.bat
- cap_rect_cursorshake_short.bat
- cap_rect_disable_cursorshake.bat
- cap_rect_randomly.bat

### Use from AutoHotkey

```ahk
; Capture the active window with Win + A key.
#a::run,pythonw D:\work\github\stakiran\commandcap\commandcap.py -a -o D:\data\screenshots --format "$2"
```

The important point is to use `pythonw` for hiding command prompt window.

## Usage

```
$ python commandcap.py -h
usage: commandcap.py [-h] [-f] [-a] [-r RECT] [-j] [-p] [-o OUTPUT_DIRECTORY]
                     [--format FORMAT] [--format1 FORMAT1] [--format2 FORMAT2]
                     [-w WAIT] [--disable-cursorshake]
                     [--cursorshake-count CURSORSHAKE_COUNT]
                     [--cursorshake-distance CURSORSHAKE_DISTANCE] [-t]

Simple light commandline screen capture tool.

optional arguments:
  -h, --help            show this help message and exit
  -f, --fullscreen
  -a, --activewindow
  -r RECT, --rect RECT  Must be given with `top,left,right,bottom` by pixel.
                        (default: 0,0,100,100)
  -j, --jpeg            Generate the image with JPEG. (default: True)
  -p, --png             Generate the image with PNG. This option disable to
                        --jpeg. (default: False)
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        An output directory of captured image. (default:
                        D:\work\github\stakiran_sub\commandcap)
  --format FORMAT       A filename format. You can use slot1 as `$1` and slot2
                        as `$2` (default: $2)
  --format1 FORMAT1     A format placeholder of today datetime string based on
                        strftime. slot1. (default: %Y/%m/%d %H:%M:%S)
  --format2 FORMAT2     A format placeholder of today datetime string based on
                        strftime. slot2. (default: %y%m%d_%H%M%S)
  -w WAIT, --wait WAIT  Do sleep before capturing. (default: 0)
  --disable-cursorshake
                        Disable the cursor-shake for notifying success of
                        capturing. (default: False)
  --cursorshake-count CURSORSHAKE_COUNT
                        cursor-shake parameter: A count of shaking. (default:
                        10)
  --cursorshake-distance CURSORSHAKE_DISTANCE
                        cursor-shake parameter: A distance of mouse cursor
                        moving when shaking. (default: 10)
  -t, --test            Show output filename only. (not saving image.)
                        (default: False)
```

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
