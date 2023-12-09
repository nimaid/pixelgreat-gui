import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

from . import windows, constants


# Main window class
#   Handles variables related to the main window.
#   Any actual program functionality or additional dialogs are handled elsewhere
class MainWindow:
    def __init__(self, qt_args):
        # Make main objects
        self.app = QApplication(qt_args)
        self.window = windows.MyQMainWindow()

        # Declare variables
        self.padding_px = 10

        # Setup colors
        self.app.setStyle("fusion")

        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(constants.COLORS["background"]))
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.Base, QColor(constants.COLORS["foreground"]))
        self.palette.setColor(QPalette.AlternateBase, QColor(constants.COLORS["foreground"]))
        self.palette.setColor(QPalette.ToolTipBase, Qt.black)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.Button, QColor(constants.COLORS["foreground"]))
        self.palette.setColor(QPalette.ButtonText, Qt.white)
        self.palette.setColor(QPalette.BrightText, Qt.red)
        self.palette.setColor(QPalette.Link, QColor(constants.COLORS["link"]))
        self.palette.setColor(QPalette.Highlight, QColor(constants.COLORS["link"]))
        self.palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(self.palette)

    def run(self):
        self.window.show()
        self.app.exec()


def run(args=None):
    if args is None:
        args = sys.argv
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"
    main_window = MainWindow(args)
    main_window.run()
