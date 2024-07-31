from typing import List

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import utils
from models.Deck import Deck
from widgets.CardWidget import CardWidget
from theme import deck_list_item_font, palette, default_text_font


class DeckListWidget(QWidget):
    """
    This widget displays a list of decks that the user can choose from. When the user clicks a button, the deck is
    displayed in a CardWidget for review.
    """

    def __init__(self, decks: List[Deck]):
        """
        Initialize the DeckListWidget with a list of decks.
        :param decks: The list of decks to display
        """
        super().__init__()
        self.settings = utils.load_config("settings.ini")
        self.max_reviews = self.settings.getint("USER", "daily_reviews_limit", fallback=100)
        self.max_new = self.settings.getint("USER", "new_card_limit", fallback=10)
        self.remaining_card_count = None

        self.decks = decks
        self.layout = QVBoxLayout()
        self.deck_list_widget = QWidget()
        self.deck_list_widget.font = deck_list_item_font
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

        self.remaining_card_count_label = QLabel()
        self.remaining_card_count_label.alignment = Qt.AlignCenter
        self.remaining_card_count_label.font = default_text_font
        self.remaining_card_count_label.style_sheet = f"color: {palette['text'].name()}"
        self.layout.add_widget(self.remaining_card_count_label)

        utils.setup_shortcuts(self, shortcuts={
            "Esc": lambda: self.stacked_widget.set_current_widget(self.deck_list_widget)
        })

        self.set_layout(self.layout)

    @Slot()
    def view_deck(self, deck: Deck):
        """
        Switch to the CardWidget view for the selected deck.
        :param deck: The deck to view
        :return: None
        """

        filtered_cards, num_cards_remaining = deck.get_filtered_cards(self.max_reviews, self.max_new)
        filtered_deck = Deck(deck.name, filtered_cards)

        self.remaining_card_count = num_cards_remaining
        self.remaining_card_count_label.text = f'Remaining cards: <span style="color: {palette["primary_400"].name()}">{self.remaining_card_count}</span>'
        self.remaining_card_count_label.show()
        # Mark the deck as modified so that it is saved when the user exits the application
        deck.is_modified = True
        # Create a new widget to house the card widget
        flashcard_layout_widget = QWidget()
        flashcard_layout = QVBoxLayout(flashcard_layout_widget)
        card_widget = CardWidget(filtered_deck)

        # If a deck has already been viewed, disconnect the card_passed signal from the CardWidget and reconnect it to the handle_card_review method
        if self.stacked_widget.count > 1:
            card_widget.signals.card_passed.disconnect()
        card_widget.signals.card_passed.connect(self.handle_card_review)

        # Create a back button to return to the deck list
        back_button = QPushButton("Back")
        back_button.tool_tip = "Shortcut: Esc"
        back_button.clicked.connect(lambda: self.stacked_widget.set_current_widget(self.deck_list_widget))

        # Add the back button and card widget to the flashcard layout
        flashcard_layout.add_widget(back_button)
        flashcard_layout.add_widget(card_widget)
        self.stacked_widget.add_widget(flashcard_layout_widget)
        self.stacked_widget.set_current_widget(flashcard_layout_widget)

    def handle_card_review(self):
        self.remaining_card_count -= 1
        self.remaining_card_count_label.text = f'Remaining cards: <span style="color: {palette["primary_400"].name()}">{self.remaining_card_count}</span>'