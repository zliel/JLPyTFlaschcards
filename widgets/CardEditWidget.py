from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Flashcard import Flashcard


class CardEditWidget(QWidget):
    def __init__(self, card: Flashcard = None) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.card = card

        self.front_label = QLabel("Front:")
        self.layout.add_widget(self.front_label)
        self.front_input = QLineEdit()
        self.layout.add_widget(self.front_input)

        self.back_label = QLabel("Back:")
        self.layout.add_widget(self.back_label)
        self.back_input = QLineEdit()
        self.layout.add_widget(self.back_input)

        self.tags_label = QLabel("Tags (seperate by spaces):")
        self.layout.add_widget(self.tags_label)
        self.tags_input = QLineEdit()
        self.layout.add_widget(self.tags_input)

        self.save_button = QPushButton("Save")
        self.layout.add_widget(self.save_button)

        self.set_layout(self.layout)

        if self.card:
            self.load_card()
        # self.show()

    def load_card(self):
        self.front_input.text = self.card.question
        self.back_input.text = self.card.answer
        # example: "tag1 tag2 tag3"
        self.tags_input.text = " ".join(self.card.tags)
