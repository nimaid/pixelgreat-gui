from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QHBoxLayout,
    QLabel, QPushButton,
    QFileDialog, QAction,
    QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox,
    QSpinBox, QDoubleSpinBox,
    QMessageBox,
    QAbstractButton,
    QSlider,
    QStyle,
    QProgressDialog
)
from PyQt5.QtGui import (
    QImage, QPixmap, QIcon,
    QPainter
)

import constants


# ---- MAIN WINDOW ----

# My QMainWindow class
#   Used to customize the main window.
class MyQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup window title and icon
        self.setWindowTitle(f"{constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATHS["program"]))

        # Declare elements
        self.padding_px = 10

        self.test_label = QLabel("Wow! TEEEEEEESSSST")
        self.test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Declare main layout
        self.main_layout = QGridLayout()
        self.main_layout.setContentsMargins(self.padding_px, self.padding_px, self.padding_px, self.padding_px)
        self.main_layout.setSpacing(self.padding_px)

        # Populate main layout
        self.main_layout.addWidget(self.test_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set main layout as the central widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Declare a menu bar
        self.main_menu = self.menuBar()

        # Declare a "File" menu
        self.file_menu = self.main_menu.addMenu("File")

        # Populate the "File" menu
        self.file_menu_open = QAction("Open...", self)
        self.file_menu_open.triggered.connect(self.open_file_clicked)
        self.file_menu.addAction(self.file_menu_open)

        self.file_menu_close = QAction("Close", self)
        self.file_menu_close.triggered.connect(self.close_file_clicked)
        self.file_menu.addAction(self.file_menu_close)

        # Set window to content size
        self.resize_window()

        # Initialize other variables
        self.filename = None

    def resize_window(self):
        size_hint = self.sizeHint()
        self.setFixedSize(size_hint)

    def open_file_clicked(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            "Open File",
            constants.PROG_PATH,
            "All Binary Files (*)"
        )

        if filename != "":
            print(f"Open {filename}")
            self.filename = filename

    def close_file_clicked(self):
        print(f"Close {self.filename}")
        self.filename = None
