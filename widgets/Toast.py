from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot, QTimer

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property


class Toast(QLabel):
    def __init__(self):
        super().__init__()
        self.window_flag = Qt.FramelessWindowHint

        self.alignment = Qt.AlignCenter
        self.timer = QTimer(parent=self)
        self.timer.single_shot = True
        self.timer.timeout.connect(self.hide)

    def show_toast(self, message: str, duration: int = 2000):
        self.text = message
        self.show()
        self.timer.start(duration)

