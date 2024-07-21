from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt, Slot, Signal, QObject, QEvent

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

import utils
from models.Deck import Deck
from models.Flashcard import Flashcard
from widgets.CardEditWidget import CardEditWidget


class CardBrowserSignals(QObject):
    """ This class defines the signals that will be used by the CardBrowserWidget. """
    closed = Signal()


class CardBrowserWidget(QWidget):
    """ This class defines the CardBrowserWidget, which will allow the user to browse the cards in the application. """
    signals = CardBrowserSignals()

    def __init__(self, app_decks: list[Deck]):
        """
        Initializes the CardBrowserWidget with the given list of decks.
        :param app_decks: The list of decks to display cards from
        """
        super().__init__()

        self.window_title = "Browse Cards"
        self.layout = QHBoxLayout()
        # Keep a copy of all decks for filtering
        self.all_decks = app_decks
        # Starts with all decks
        self.current_deck_list = app_decks
        self.deck_lookup = {deck.name: deck for deck in self.all_decks}
        self.filter_cache = {}
        self.build_tag_index()

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

        self.card_tree_widget = QTreeWidget()
        self.card_tree_widget.set_header_labels(["Front", "Back", "Tags"])
        self.update_card_list(self.current_deck_list)

        self.card_tree_widget.itemDoubleClicked.connect(lambda item: self.show_card_editor(item))
        self.layout.add_widget(self.card_tree_widget)

        self.card_edit_widget = CardEditWidget()

        self.set_layout(self.layout)
        utils.setup_shortcuts(self, shortcuts={
            "Esc": self.close,
            "Del": self.delete_card
        })

        # Handle closeEvents
        self.install_event_filter(self)

        self.show()

    def generate_tag_list(self, app_decks: list[Deck]) -> list[str]:
        """
        Generates a list of all tags in the decks
        :param app_decks: The list of decks to generate tags from
        :return: A sorted list of tags
        """
        tags = set()
        for deck in app_decks:
            for card in deck.cards:
                tags.update(card.tags)
        return sorted(list(tags))

    def select_filter(self, item: QListWidgetItem):
        """
        Filters the card list based on the selected item. If the item is a deck name, only cards from that deck will be shown.
        If the item is a tag, only cards with that tag will be shown, regardless of the deck they belong to.
        :param item: The item that was double-clicked in the QListWidget
        :return: None
        """
        item_text = item.text()

        if item_text in ("-- All Decks --", "-- All Tags --"):
            self.current_deck_list = self.all_decks
        else:
            # Check if the item is a deck name or a tag
            if item_text in self.deck_lookup:
                self.current_deck_list = [self.deck_lookup[item_text]]
            elif item_text in self.tag_list:
                self.current_deck_list = [deck for deck in self.all_decks if
                                          any(card in self.tag_to_cards[item_text] for card in deck.cards)]
            else:
                self.current_deck_list = []

        if item_text != "-- All Decks --" and item_text != "-- All Tags --":
            self.filter_cache[item_text] = self.current_deck_list
        self.update_card_list(self.current_deck_list)

    def event_filter(self, obj, event):
        """
        Checks incoming events for the close event, and emits the closed signal if it is detected
        :param obj: The target of the event
        :param event: The event being processed
        :return: None
        """
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
        """
        Shows the card editor widget for the selected card.
        :param item: The item that was double-clicked in the QListWidget
        :return: None
        """
        card = item.data(0, Qt.UserRole)
        if self.card_edit_widget:
            self.card_edit_widget.close()
            self.card_edit_widget.delete_later()
        self.card_edit_widget = CardEditWidget(card)
        self.card_edit_widget.signals.card_edited.connect(self.handle_card_update)
        self.layout.add_widget(self.card_edit_widget)

    @Slot(Flashcard)
    def handle_card_update(self, updated_card):
        """
        Updates the card in the deck and refreshes the card list.
        :param updated_card: The updated card
        :return: None
        """
        # The card will automatically be updated in the deck, as the card is passed by reference,
        # but we need to make sure the deck it belongs to is marked as modified
        affected_filters = set(updated_card.tags)
        # Optionally, add the deck name if it's relevant to your filtering logic
        for deck in self.all_decks:
            if updated_card in deck.cards:
                affected_filters.add(deck.name)
                deck.is_modified = True
                break

        # Update cache accordingly
        self.update_filter_cache(affected_filters)

        self.update_card_list(self.current_deck_list)

    def update_card_list(self, current_deck_list):
        """
        Updates the card list widget with the cards from the current deck list, and sets the selected index to the last card selected.
        :param current_deck_list: The list of decks to display cards from
        :return: None
        """
        # figure out which card, if any, is currently selected
        selected_card = None
        if self.card_tree_widget.current_item():
            selected_card = self.card_tree_widget.current_item().data(0, Qt.UserRole)

        self.card_tree_widget.clear()
        for deck in current_deck_list:
            for card in deck.cards:
                card_item = QTreeWidgetItem()
                card_item.set_text(0, card.question)
                card_item.set_text(1, card.answer)
                card_item.set_text(2, ", ".join(card.tags))
                card_item.set_data(0, Qt.UserRole, card)
                self.card_tree_widget.add_top_level_item(card_item)

        # Select the last selected card
        if selected_card:

            for i in range(self.card_tree_widget.top_level_item_count):
                item = self.card_tree_widget.top_level_item(i)
                if item.data(0, Qt.UserRole).id == selected_card.id:
                    self.card_tree_widget.set_current_item(item)
                    break
        else:
            # Select the first card
            self.card_tree_widget.set_current_item(self.card_tree_widget.top_level_item(0))
        # NOTE: This could pose a problem when we allow deleting cards, as the index could be out of bounds
        # This could also be a problem when filtering

    def build_tag_index(self):
        """
        Builds a reverse index from tags to cards.
        """
        self.tag_to_cards = {}
        for deck in self.all_decks:
            for card in deck.cards:
                for tag in card.tags:
                    if tag not in self.tag_to_cards:
                        self.tag_to_cards[tag] = set()
                    self.tag_to_cards[tag].add(card)

    def filter_cards_by_tag(self, tag):
        """
        Returns a list of cards that have the specified tag, using the reverse index.
        """
        if tag in self.tag_to_cards:
            return list(self.tag_to_cards[tag])
        return []

    def delete_card(self):
        """
        Deletes the selected card from the deck and refreshes the card list.
        """
        selected_item = self.card_tree_widget.current_item()
        if selected_item:
            selected_card = selected_item.data(0, Qt.UserRole)
            for deck in self.all_decks:
                if selected_card in deck.cards:
                    deck.cards.remove(selected_card)
                    deck.is_modified = True
                    break

            self.update_filter_cache(set(selected_card.tags))

            self.update_card_list(self.current_deck_list)

    def update_filter_cache(self, affected_filters):
        for filter_key in list(self.filter_cache.keys()):
            if filter_key in affected_filters or filter_key == "-- All Decks --":
                self.filter_cache.pop(filter_key, None)
