#!/usr/bin/env python3

import sys
from PIL import Image
import pixelgreat as pg
from PyQt5.QtWidgets import QApplication


import windows


# Main window class
#   Handles variables related to the main window.
#   Any actual program functionality or additional dialogs are
#   handled using different classes
class MainWindow:
    def __init__(self, qt_args):
        self.app = QApplication(qt_args)
        self.window = windows.MyQMainWindow()

    def run(self):
        self.window.show()
        self.app.exec()


def main(args):
    main_window = MainWindow(args)
    main_window.run()


def run():
    main(sys.argv)


if __name__ == "__main__":
    run()
