import math
from PyQt5.QtWidgets import QSlider, QStyle


# Custom seekbar class
#   A customized slider
class SeekBar(QSlider):
    def __init__(self,
                 parent=None,
                 position_changed_callback=None,
                 handle_size=10,
                 color="#666",
                 hover_color="#000"
                 ):
        super(SeekBar, self).__init__(parent)

        self.handle_size = handle_size
        # TODO: Fix handle width not changing
        # TODO: Fix handle not hanging over the side

        self.setFixedHeight(self.handle_size)

        self.setStyleSheet(
            "QSlider::handle {{ background: {2}; height: {0}px; width: {0}px; border-radius: {1}px; }} "
            "QSlider::handle:hover {{ background: {3}; height: {0}px; width: {0}px; border-radius: {1}px; }}".format(
                self.handle_size,
                math.floor(self.handle_size / 2),
                color,
                hover_color
            )
        )

        self.position_changed_callback = position_changed_callback

    def set_position(self, value, do_callback=True):
        if self.position_changed_callback is not None and do_callback:
            self.position_changed_callback(value)

        self.setValue(value)

    def mousePressEvent(self, event):
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.set_position(value)

    def mouseMoveEvent(self, event):
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.set_position(value)
