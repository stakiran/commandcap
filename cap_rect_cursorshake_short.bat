@echo off
setlocal
python commandcap.py --format "rect_cursorshake_short_$2" --cursorshake-count 3 --cursorshake-distance 1
