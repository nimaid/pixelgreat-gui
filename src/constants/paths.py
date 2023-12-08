import os
import sys

# Test if this is a PyInstaller executable or a .py file
if getattr(sys, 'frozen', False):
    IS_EXE = True
    PROG_FILE = sys.executable
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = sys._MEIPASS
else:
    IS_EXE = False
    PROG_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    PROG_FILE = os.path.join(PROG_PATH, "pixelgreat-gui.py")
    PATH = PROG_PATH
