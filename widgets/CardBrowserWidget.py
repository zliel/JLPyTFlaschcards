from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
from models.Flashcard import Flashcard
from widgets.CardEditWidget import CardEditWidget


class CardBrowserWidget(QWidget):
    def __init__(self, app_decks: list[Deck]):
        super().__init__()
        self.window_title = "Browse Cards"
        self.layout = QHBoxLayout()
        # Keep a copy of all decks for filtering
        self.all_decks = app_decks
        # Starts with all decks
        self.current_deck_list = app_decks

        # Note: when filtering, you should update the current_deck_list to some subset of app_decks, so they stay in sync
        self.filter_list_widget = QListWidget()
        self.layout.add_widget(self.filter_list_widget)

        self.card_list_widget = QListWidget()
        self.update_card_list(self.current_deck_list)

        self.card_list_widget.itemDoubleClicked.connect(lambda item: self.show_card_editor(item))
        self.layout.add_widget(self.card_list_widget)

        self.card_edit_widget = CardEditWidget()
        # self.layout.add_widget(self.card_edit_widget)

        self.set_layout(self.layout)
        self.show()

    @Slot()
    def show_card_editor(self, item):
        card = item.data(Qt.UserRole)
        if self.card_edit_widget:
            self.card_edit_widget.close()
        self.card_edit_widget = CardEditWidget(card)
        self.card_edit_widget.signals.card_edited.connect(self.handle_card_update)
        self.layout.add_widget(self.card_edit_widget)

    @Slot(Flashcard)
    def handle_card_update(self, updated_card):
        # The card will automatically be updated in the deck, as the card is passed by reference,
        # but we need to make sure the deck it belongs to is marked as modified
        for deck in self.all_decks:
            for card in deck.cards:
                if card.id == updated_card.id:
                    deck.is_modified = True

        self.update_card_list(self.current_deck_list)

    def update_card_list(self, current_deck_list):
        last_card_selected = self.card_list_widget.current_index()
        self.card_list_widget.clear()
        for deck in current_deck_list:
            for card in deck.cards:
                item = QListWidgetItem(f"{card.question} - {card.answer}")
                item.set_data(Qt.UserRole, card)
                self.card_list_widget.add_item(item)

        self.card_list_widget.set_current_index(last_card_selected)
        # NOTE: This could pose a problem when we allow deleting cards, as the index could be out of bounds
        # This could also be a problem when filtering


