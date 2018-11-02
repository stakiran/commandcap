@echo off
setlocal
set /a x1=%random%%%1024
set /a y1=%random%%%768
set /a x2=%x1%+%random%%%1024
set /a y2=%y1%+%random%%%768
python commandcap.py --format "rect_$2" -r %x1%,%y1%,%x2%,%y2%
