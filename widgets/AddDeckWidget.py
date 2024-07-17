from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property


class AddDeckWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.window_title = "Add a deck"
        self.layout = QVBoxLayout()

        self.deck_name_label = QLabel("Deck Name:")
        self.layout.add_widget(self.deck_name_label)
        self.deck_name_input = QLineEdit()
        self.layout.add_widget(self.deck_name_input)

        self.add_deck_button = QPushButton("Add Deck")
        self.layout.add_widget(self.add_deck_button)

        self.set_layout(self.layout)
        self.resize(400, 300)
        self.show()
