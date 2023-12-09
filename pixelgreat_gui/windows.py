import pixelgreat as pg
from PIL import Image
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton,
    QFileDialog, QAction, QSizePolicy,
    QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox,
    QSpinBox, QDoubleSpinBox,
    QMessageBox, QTextEdit,
    QAbstractButton,
    QSlider,
    QStyle,
    QProgressDialog,
    QGraphicsView
)
from PyQt5.QtGui import (
    QImage, QPixmap, QIcon,
    QPainter, QColor, QPalette
)

from . import constants, helpers, widgets, settings


# ---- MAIN WINDOW ----

# My QMainWindow class
#   Used to customize the main window.
class MyQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup window title and icon
        self.setWindowTitle(f"{constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATHS["program"]))

        # Declare variables
        self.padding_px = 10
        self.filename = None
        self.source = None

        # Make main settings object
        self.settings = settings.PixelgreatSettings()

        # Set main window size restrictions
        self.setMinimumSize(300, 300)
        self.resize(800, 600)

        # Setup main viewer
        self.viewer = widgets.PhotoViewer(self, background=QColor(constants.COLORS["viewer"]))
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Declare settings elements
        #   Screen Type
        self.screen_type_entry_label = QLabel("Screen Type:")
        self.screen_type_entry = QComboBox()
        self.screen_type_entry.addItems(["LCD", "CRT TV", "CRT Monitor"])
        if self.settings.get_screen_type() == pg.ScreenType.LCD:
            self.screen_type_entry.setCurrentIndex(0)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_TV:
            self.screen_type_entry.setCurrentIndex(1)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_MONITOR:
            self.screen_type_entry.setCurrentIndex(2)
        self.screen_type_entry.currentIndexChanged.connect(self.screen_type_entry_changed)
        #   Pixel Padding
        self.pixel_padding_entry_label = QLabel("Pixel Padding:")
        self.pixel_padding_entry = QDoubleSpinBox()
        self.pixel_padding_entry.setMinimum(0.0)
        self.pixel_padding_entry.setMaximum(100.0)
        self.pixel_padding_entry.setSingleStep(1.0)
        self.pixel_padding_entry.setSuffix("%")
        self.pixel_padding_entry.setValue(self.settings.get_setting("pixel_padding") * 100)
        self.pixel_padding_entry.valueChanged.connect(self.pixel_padding_entry_changed)
        #   Grid Direction
        self.direction_entry_label = QLabel("Grid Direction:")
        self.direction_entry = QComboBox()
        self.direction_entry.addItems(["Vertical", "Horizontal"])
        if self.settings.get_setting("direction") == pg.Direction.VERTICAL:
            self.direction_entry.setCurrentIndex(0)
        elif self.settings.get_setting("direction") == pg.Direction.HORIZONTAL:
            self.direction_entry.setCurrentIndex(1)
        self.direction_entry.currentIndexChanged.connect(self.direction_entry_changed)
        #   Washout
        self.washout_entry_label = QLabel("Washout:")
        self.washout_entry = QDoubleSpinBox()
        self.washout_entry.setMinimum(0.0)
        self.washout_entry.setMaximum(100.0)
        self.washout_entry.setSingleStep(1.0)
        self.washout_entry.setSuffix("%")
        self.washout_entry.setValue(self.settings.get_setting("washout") * 100)
        self.washout_entry.valueChanged.connect(self.washout_entry_changed)
        #   Brighten
        self.brighten_entry_label = QLabel("Brighten:")
        self.brighten_entry = QDoubleSpinBox()
        self.brighten_entry.setMinimum(0.0)
        self.brighten_entry.setMaximum(100.0)
        self.brighten_entry.setSingleStep(1.0)
        self.brighten_entry.setSuffix("%")
        self.brighten_entry.setValue(self.settings.get_setting("brighten") * 100)
        self.brighten_entry.valueChanged.connect(self.brighten_entry_changed)
        #   Blur
        self.blur_entry_label = QLabel("Blur:")
        self.blur_entry = QDoubleSpinBox()
        self.blur_entry.setMinimum(0.0)
        self.blur_entry.setMaximum(100.0)
        self.blur_entry.setSingleStep(1.0)
        self.blur_entry.setSuffix("%")
        self.blur_entry.setValue(self.settings.get_setting("blur") * 100)
        self.blur_entry.valueChanged.connect(self.blur_entry_changed)

        # Declare settings area
        self.settings_area = QGridLayout()
        self.settings_area.setContentsMargins(0, 0, 0, self.padding_px)
        self.settings_area.setSpacing(self.padding_px)

        # Populate settings area
        self.entries_array = [
            [  # Column 0-1
                [self.screen_type_entry_label, self.screen_type_entry],
                [self.blur_entry_label, self.blur_entry]
            ],
            [  # Column 2-3
                [self.washout_entry_label, self.washout_entry],
                [self.direction_entry_label, self.direction_entry],
            ],
            [  # Column 4-5
                [self.pixel_padding_entry_label, self.pixel_padding_entry],
                [self.brighten_entry_label, self.brighten_entry]
            ]
        ]
        for column, column_group in enumerate(self.entries_array):
            for row, row_group in enumerate(column_group):
                self.settings_area.addWidget(
                    row_group[0],
                    row,
                    column * 2,
                    alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
                )
                self.settings_area.addWidget(
                    row_group[1],
                    row,
                    (column * 2) + 1,
                    alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )

        # Start the settings area disabled
        self.set_settings_entries_enabled(False)

        # Declare main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(self.padding_px)

        # Populate main layout
        self.main_layout.addWidget(self.viewer)
        self.main_layout.addLayout(self.settings_area)

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

    def set_viewer_image(self, image=None):
        if image is not None:
            self.viewer.set_photo(helpers.image_to_pixmap(image))
        else:
            self.viewer.set_photo(None)

    def set_source(self, filename=None):
        self.filename = filename
        if self.filename is not None:
            self.source = Image.open(self.filename)
            self.set_viewer_image(self.source)
            self.set_settings_entries_enabled(True)
        else:
            self.set_viewer_image(None)
            self.set_settings_entries_enabled(False)

    def set_settings_entries_enabled(self, enabled):
        for element in [
            self.screen_type_entry,
            self.direction_entry,
            self.washout_entry,
            self.pixel_padding_entry,
            self.brighten_entry,
            self.blur_entry
        ]:
            element.setEnabled(enabled)

    # Called when the Screen Type is changed
    # Therefore, the Screen Type entry is NOT updated here
    def update_settings_entries(self):
        if self.settings.get_setting("direction") == pg.Direction.VERTICAL:
            self.direction_entry.setCurrentIndex(0)
        elif self.settings.get_setting("direction") == pg.Direction.HORIZONTAL:
            self.direction_entry.setCurrentIndex(1)

        # Set the percentage inputs
        for element, name in [
            [self.washout_entry, "washout"],
            [self.pixel_padding_entry, "pixel_padding"],
            [self.brighten_entry, "brighten"],
            [self.blur_entry, "blur"]
        ]:
            element.setValue(self.settings.get_setting(name) * 100)

    def screen_type_entry_changed(self, idx):
        if idx == 0:
            self.settings.set_screen_type(pg.ScreenType.LCD)
        elif idx == 1:
            self.settings.set_screen_type(pg.ScreenType.CRT_TV)
        elif idx == 2:
            self.settings.set_screen_type(pg.ScreenType.CRT_MONITOR)

        self.update_settings_entries()

    def direction_entry_changed(self, idx):
        if idx == 0:
            self.settings.set_setting("direction", pg.Direction.VERTICAL)
        elif idx == 1:
            self.settings.set_setting("direction", pg.Direction.HORIZONTAL)

    def washout_entry_changed(self, value):
        self.settings.set_setting("washout", value / 100)

    def pixel_padding_entry_changed(self, value):
        self.settings.set_setting("pixel_padding", value / 100)

    def brighten_entry_changed(self, value):
        self.settings.set_setting("brighten", value / 100)

    def blur_entry_changed(self, value):
        self.settings.set_setting("blur", value / 100)

    def open_file_clicked(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            "Open File",
            constants.PROG_PATH,
            "Image Files (*.png *.jpg *.bmp)"
        )

        if filename != "":
            self.set_source(filename)

    def close_file_clicked(self):
        self.set_source(None)

    def about_clicked(self):
        popup = About(parent=self)

        result = popup.exec()

    def resizeEvent(self, event):
        self.viewer.update_view()


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
            f"Project Home Page:\n{constants.PROJECT_URL}\n\n"
            f"Patreon:\n{constants.DONATE_URL}")
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
