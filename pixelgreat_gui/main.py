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


def run(args=None):
    if args is None:
        args = sys.argv
    main_window = MainWindow(args)
    main_window.run()
