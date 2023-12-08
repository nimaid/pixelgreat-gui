#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from . import windows


# Main window class
#   Handles variables related to the main window.
#   Any actual program functionality or additional dialogs are handled elsewhere
class MainWindow:
    def __init__(self, qt_args):
        self.app = QApplication(qt_args)
        self.window = windows.MyQMainWindow()

    def run(self):
        self.window.show()
        self.app.exec()


def main():
    main_window = MainWindow(sys.argv)
    main_window.run()


if __name__ == "__main__":
    main()
