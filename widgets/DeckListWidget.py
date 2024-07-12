from typing import List

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from models.Deck import Deck


class DeckListWidget(QWidget):
    def __init__(self, decks: List[Deck]):
        super().__init__()
        self.decks = decks

        # Set up the layout
        self.layout = QVBoxLayout()
        self.deck_list_widget = QWidget()
        self.deck_list = QVBoxLayout(self.deck_list_widget)
        # Create a stacked widget to switch between the deck list and the card view
        self.stacked_widget = QStackedWidget()

        # Create a button for each deck
        for deck in self.decks:
            btn_name_layout = QHBoxLayout()
            deck_label = QLabel(deck.name)
            deck_label.alignment = Qt.AlignCenter
            btn_name_layout.add_widget(deck_label)

            # Connect the button to the view_deck method
            view_deck_btn = QPushButton("View Deck")
            view_deck_btn.clicked.connect(lambda clicked, current_deck=deck: self.view_deck(current_deck))
            btn_name_layout.add_widget(view_deck_btn)
            self.deck_list.add_layout(btn_name_layout)

        # Add the deck list widget to the stacked widget
        self.stacked_widget.add_widget(self.deck_list_widget)
        self.layout.add_widget(self.stacked_widget)
        self.set_layout(self.layout)

    @Slot()
    def view_deck(self, deck: Deck):
        pass
