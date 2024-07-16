from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property


class AddCardWidget(QWidget):
    def __init__(self, app_decks):
        super().__init__()
        self.layout = QVBoxLayout()

        self.decks = app_decks
        self.deck_label = QLabel("Deck:")
        self.layout.add_widget(self.deck_label)
        self.deck_dropdown = QComboBox()
        self.deck_dropdown.add_items([deck.name for deck in self.decks])
        self.layout.add_widget(self.deck_dropdown)

        self.question_label = QLabel("Front:")
        self.layout.add_widget(self.question_label)
        self.question_input = QLineEdit()
        self.layout.add_widget(self.question_input)

        self.answer_label = QLabel("Back:")
        self.layout.add_widget(self.answer_label)
        self.answer_input = QLineEdit()
        self.layout.add_widget(self.answer_input)

        self.add_card_button = QPushButton("Add Card")
        # self.add_card_button.clicked.connect(self.add_card)
        self.layout.add_widget(self.add_card_button)

        self.set_layout(self.layout)
        self.resize(400, 300)
        self.show()