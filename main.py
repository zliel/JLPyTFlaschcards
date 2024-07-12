import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property


my_app = QApplication([])

class MainWindow(QWidget):
    """This class defines the main window of the application, which will house all other necessary widgets."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to JLPyTFlashcards, your hub for practicing your JLPT Vocabulary")
        welcome_label.alignment = Qt.AlignCenter
        self.layout.add_widget(welcome_label)
        self.set_layout(self.layout)

        self.window_title = "JLPyT Flashcards"
        self.resize(1200, 700)
        self.palette = Qt.black


main_window = MainWindow()
main_window.show()

sys.exit(my_app.exec())
