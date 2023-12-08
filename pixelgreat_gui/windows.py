from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
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

from . import constants


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

        # TODO: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
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

        # Declare the "Help" menu
        self.help_menu = self.main_menu.addMenu("Help")

        # Populate the "Help" menu
        self.help_menu_about = QAction("About...", self)
        self.help_menu_about.triggered.connect(self.about_clicked)
        self.help_menu.addAction(self.help_menu_about)

        # Initialize other variables
        self.filename = None

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

    def about_clicked(self):
        popup = About(parent=self)

        result = popup.exec()

# ---- POPUP WINDOWS ----

# About dialog
#   Gives info about the program
class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"About {constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATHS["program"]))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.icon_size = 200

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setPixmap(QPixmap(constants.ICON_PATHS["program"]))
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(self.icon_size, self.icon_size)

        self.about_text = QLabel(
            f"{constants.TITLE} v{constants.VERSION}\nby {constants.COPYRIGHT}\nCopyright 2023\n\n"
            f"{constants.DESCRIPTION}\n\n"
            f"Project Home Page:\n{constants.PROJECT_URL}\n\nPatreon:\n{constants.DONATE_URL}")
        self.about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.confirm_buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.confirm_buttons.accepted.connect(self.accept)

        self.main_layout = QGridLayout()

        self.main_layout.addWidget(self.icon_label, 0, 0, 2, 1)
        self.main_layout.addWidget(self.about_text, 0, 1)
        self.main_layout.addWidget(self.confirm_buttons, 1, 0, 1, 2)

        self.setLayout(self.main_layout)

        self.resize_window()

    def resize_window(self):
        self.setFixedSize(self.sizeHint())



# ---- CUSTOM ELEMENTS ----
