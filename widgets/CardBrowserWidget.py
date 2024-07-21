from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Slot, Signal, QObject, QEvent

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

import utils
from models.Deck import Deck
from models.Flashcard import Flashcard
from widgets.CardEditWidget import CardEditWidget


class CardBrowserSignals(QObject):
    closed = Signal()


class CardBrowserWidget(QWidget):
    signals = CardBrowserSignals()

    def __init__(self, app_decks: list[Deck]):
        super().__init__()

        self.window_title = "Browse Cards"
        self.layout = QHBoxLayout()
        # Keep a copy of all decks for filtering
        self.all_decks = app_decks
        # Starts with all decks
        self.current_deck_list = app_decks
        self.deck_lookup = {deck.name: deck for deck in self.all_decks}

        # Note: when filtering, you should update the current_deck_list to some subset of app_decks, so they stay in sync
        self.filter_list_widget = QListWidget()
        self.filter_list_widget.add_item("-- All Decks --")
        for deck in app_decks:
            self.filter_list_widget.add_item(deck.name)
        self.filter_list_widget.add_item("-- All Tags --")
        self.tag_list = self.generate_tag_list(app_decks)
        self.filter_list_widget.add_items(self.tag_list)
        self.filter_list_widget.itemDoubleClicked.connect(lambda item: self.select_filter(item))

        self.layout.add_widget(self.filter_list_widget)

        self.card_list_widget = QListWidget()
        self.update_card_list(self.current_deck_list)

        self.card_list_widget.itemDoubleClicked.connect(lambda item: self.show_card_editor(item))
        self.layout.add_widget(self.card_list_widget)

        self.card_edit_widget = CardEditWidget()

        self.set_layout(self.layout)

        # Handle closeEvents
        self.install_event_filter(self)

        self.show()

    def generate_tag_list(self, app_decks):
        tags = set()
        for deck in app_decks:
            for card in deck.cards:
                tags.update(card.tags)
        return sorted(list(tags))

    def select_filter(self, item: QListWidgetItem):
        item_text = item.text()

        if item_text in ("-- All Decks --", "-- All Tags --"):
            self.current_deck_list = self.all_decks
        else:
            # Check if the item is a deck name or a tag
            if item_text in self.deck_lookup:
                self.current_deck_list = [self.deck_lookup[item_text]]
            elif item_text in self.tag_list:
                filtered_decks = set()
                for deck in self.all_decks:
                    # Check if any card in the deck has the tag
                    if any(item_text in card.tags for card in deck.cards):
                        filtered_decks.add(deck)
                self.current_deck_list = list(filtered_decks)
            else:
                self.current_deck_list = []

        self.update_card_list(self.current_deck_list)

    def event_filter(self, obj, event):
        # print(event.type())
        if obj == self and event.type() == QEvent.Close:
            # Ensure that the card editor is fully closed before emitting the signal
            if self.card_edit_widget:
                self.card_edit_widget.close()
                self.card_edit_widget.delete_later()
            self.signals.closed.emit()
            super().close()
        return False

    @Slot()
    def show_card_editor(self, item):
        card = item.data(Qt.UserRole)
        if self.card_edit_widget:
            self.card_edit_widget.close()
            self.card_edit_widget.delete_later()
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
