from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property


class CardEditWidget(QWidget):
    def __init__(self, card):
        super().__init__()
        self.layout = QVBoxLayout()

        self.front_label = QLabel("Front:")
        self.layout.add_widget(self.front_label)
        self.front_input = QLineEdit()
        self.front_input.text = card.front
        self.layout.add_widget(self.front_input)

        self.back_label = QLabel("Back:")
        self.layout.add_widget(self.back_label)
        self.back_input = QLineEdit()
        self.back_input.text = card.back
        self.layout.add_widget(self.back_input)

        self.tags_label = QLabel("Tags (seperate by spaces):")
        self.layout.add_widget(self.tags_label)
        self.tags_input = QLineEdit()
        self.tags_input.text = " ".join(card.tags)
        self.layout.add_widget(self.tags_input)

        self.save_button = QPushButton("Save")
        self.layout.add_widget(self.save_button)

        self.show()
