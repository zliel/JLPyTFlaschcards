from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot, QTimer

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from theme import default_text_font, palette

class Toast(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window_flag = Qt.ToolTip
        self.font = default_text_font
        self.style_sheet = f"background-color: {palette['dark_200'].name()}; color: {palette['text'].name()}; border-radius: 5px; padding: 3px;"

        self.alignment = Qt.AlignCenter
        self.timer = QTimer(parent=self)
        self.timer.single_shot = True
        self.timer.timeout.connect(self.hide)

    def show_toast(self, message: str, duration: int = 2000):
        self.text = message
        self.adjust_size()
        margin_bottom = 50
        margin_right = 50
        self.move(self.parent().width - self.width - margin_right, self.parent().height - self.height - margin_bottom)
        self.show()
        self.timer.start(duration)

