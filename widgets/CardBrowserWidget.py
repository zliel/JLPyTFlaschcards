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
from palettes import list_item_font


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
        self.all_cards = [card for deck in app_decks for card in deck.cards]
        self.current_card_list = self.all_cards

        self.deck_lookup = {deck.name: deck for deck in self.all_decks}
        self.build_tag_index()
        self.tag_list = self.generate_tag_list(app_decks)
        self.filter_cache = {}
        for tag in self.tag_list:
            self.filter_cache[tag] = self.filter_cards_by_tag(tag)
        self.focused_widget = None

        # Note: when filtering, you should update the current_deck_list to some subset of app_decks, so they stay in sync
        self.filter_list_widget = QListWidget()
        self.filter_list_widget.font = list_item_font
        self.filter_list_widget.clicked.connect(self.on_filter_list_clicked)
        self.update_filter_list(app_decks)
        self.filter_list_widget.itemDoubleClicked.connect(lambda item: self.select_filter(item))

        self.layout.add_widget(self.filter_list_widget)

        self.card_tree_widget = QTreeWidget()
        self.card_tree_widget.font = list_item_font
        self.card_tree_widget.set_header_labels(["Front", "Back", "Tags"])
        self.card_tree_widget.clicked.connect(self.on_card_list_clicked)
        self.update_card_list(self.current_card_list)
        self.card_tree_widget.itemDoubleClicked.connect(lambda item: self.show_card_editor(item))
        self.layout.add_widget(self.card_tree_widget)

        self.card_edit_widget = CardEditWidget()

        self.set_layout(self.layout)

        utils.setup_shortcuts(self, shortcuts={
            "Esc": self.close,
            "Del": self.handle_delete_shortcut
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
            self.current_card_list = self.all_cards
        else:
            # Check if the item is a deck name or a tag
            if item_text in self.deck_lookup:
                self.current_card_list = [card for card in self.deck_lookup[item_text].cards]
            elif item_text in self.tag_list:
                self.current_card_list = self.filter_cards_by_tag(item_text)
            else:
                self.current_card_list = []

        if item_text != "-- All Decks --" and item_text != "-- All Tags --":
            self.filter_cache[item_text] = self.current_card_list
        self.update_card_list(self.current_card_list)

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
    def handle_card_update(self, updated_card, old_card):
        """
        Updates the card in the deck and refreshes the card list.
        :param updated_card: The updated card
        :return: None
        """
        # The card will automatically be updated in the deck, as the card is passed by reference,
        # but we need to make sure the deck it belongs to is marked as modified
        affected_filters = set(updated_card.tags)
        affected_filters.update(old_card.tags)
        for deck in self.all_decks:
            if updated_card in deck.cards:
                deck.is_modified = True
                break

        # Update cache accordingly
        self.update_filter_cache(affected_filters)

        if updated_card.tags != old_card.tags:
            self.build_tag_index()

        # Handle if a new tag was added
        new_tag_exists = False
        for tag in updated_card.tags:
            if tag not in self.tag_list:
                new_tag_exists = True
                self.tag_list.append(tag)

        if new_tag_exists:
            self.update_filter_list(self.all_decks)

        self.update_card_list(self.current_card_list)

    def update_filter_cache(self, affected_filters):
        """
        Updates the filter cache with the given set of affected filters.
        :param affected_filters: The set of filters that have been affected
        :return: None
        """
        for filter in affected_filters:
            if filter in self.filter_cache:
                self.filter_cache[filter] = self.filter_cards_by_tag(filter)

    def update_card_list(self, current_card_list):
        """
        Updates the card list widget with the cards from the current deck list, and sets the selected index to the last card selected.
        :param current_card_list: The list of decks to display cards from
        :return: None
        """
        # figure out which card, if any, is currently selected
        selected_card = None
        if self.card_tree_widget.current_item():
            selected_card = self.card_tree_widget.current_item().data(0, Qt.UserRole)

        self.card_tree_widget.clear()

        for card in current_card_list:
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
        for card in self.all_cards:
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

    @Slot()
    def on_card_list_clicked(self):
        """
        Handles the card list click event by updating the focused widget.
        """
        self.focused_widget = self.card_tree_widget

    @Slot()
    def on_filter_list_clicked(self):
        """
        Handles the filter list click event by updating the focused widget.
        """
        self.focused_widget = self.filter_list_widget

    def handle_delete_shortcut(self):
        """
        Handles the delete shortcut by deleting the selected item in the focused widget.
        :return: None
        """
        if self.focused_widget == self.card_tree_widget:
            self.delete_card()
        elif self.focused_widget == self.filter_list_widget:
            self.delete_filter()

    def delete_card(self):
        """
        Deletes the selected card from the deck and refreshes the card list.
        :return: None
        """
        selected_item = self.card_tree_widget.current_item()
        if selected_item:
            selected_card = selected_item.data(0, Qt.UserRole)
            for deck in self.all_decks:
                if selected_card in deck.cards:
                    deck.cards.remove(selected_card)
                    deck.is_modified = True

                    # Cards seemingly have to be removed from the all_cards list as well as the current_card_list
                    self.all_cards.remove(selected_card)
                    if selected_card in self.current_card_list:
                        self.current_card_list.remove(selected_card)

            self.update_card_list(self.current_card_list)
            # Update the filter list just in case the card deleted was the only one with a certain tag
            self.update_filter_list(self.all_decks)
            # Update the filter cache and tag-to-card index to remove the card from any tag filters
            self.update_filter_cache(selected_card.tags)
            self.build_tag_index()

    def delete_filter(self):
        """
        Deletes the selected tag from the deck and refreshes the card list.
        :return: None
        """
        selected_item = self.filter_list_widget.current_item()

        # Check if the item is a deck name or a tag and handle accordingly
        if selected_item:
            selected_filter = selected_item.text()
            if selected_filter in self.tag_list:
                self.delete_tag(selected_filter, selected_item)
            elif selected_filter in self.deck_lookup:
                self.delete_deck(selected_filter, selected_item)

    def delete_deck(self, selected_filter, selected_item):
        """
        Deletes the selected deck from the deck list and refreshes the card list.
        :param selected_filter: The deck name to delete, taken from the filter list
        :param selected_item: The QListWidgetItem to delete, whose text should match the selected_filter
        :return: None
        """
        # Remove the deck from the filter list
        self.filter_list_widget.remove_item_widget(selected_item)

        # Remove the deck from the all_decks list, the deck_lookup, and update the current_card_list
        deck = self.deck_lookup[selected_filter]
        self.all_cards = [card for card in self.all_cards if card not in deck.cards]
        self.current_card_list = [card for card in self.current_card_list if card not in deck.cards]
        self.all_decks.remove(deck)
        self.deck_lookup.pop(selected_filter)

        # Update the card list, filter cache and tag-to-card index to remove the cards from any tag filters
        self.update_card_list(self.current_card_list)
        self.update_filter_list(self.all_decks)
        self.build_tag_index()

    def delete_tag(self, selected_filter, selected_item):
        """
        Deletes the selected tag from the tag list and refreshes the card list.
        :param selected_filter: The tag to delete, taken from the filter list
        :param selected_item: The QListWidgetItem to delete, whose text should match the selected_filter
        :return: None
        """
        # Remove the tag from the filter list and tag list
        self.tag_list.remove(selected_filter)
        self.filter_list_widget.remove_item_widget(selected_item)

        # Remove the tag from all cards and make sure the decks that have cards with the tag are marked as modified
        for deck in self.all_decks:
            for card in deck.cards:
                if selected_filter in card.tags:
                    card.tags.remove(selected_filter)
                    deck.is_modified = True

        # Update the card list, filter cache and tag-to-card index to remove the cards from the tag filter
        self.build_tag_index()
        self.update_card_list(self.current_card_list)
        self.update_filter_list(self.all_decks)

    def update_filter_list(self, app_decks):
        """
        Updates the filter list widget with the given list of decks.
        :param app_decks: The list of decks to pull the names and tags from
        :return: None
        """
        self.filter_list_widget.clear()
        self.filter_list_widget.add_item("-- All Decks --")
        for deck in app_decks:
            self.filter_list_widget.add_item(deck.name)
        self.filter_list_widget.add_item("-- All Tags --")
        self.tag_list = self.generate_tag_list(app_decks)
        self.filter_list_widget.add_items(self.tag_list)
