from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
from widgets.CardEditWidget import CardEditWidget


class CardBrowserWidget(QWidget):
    def __init__(self, app_decks: list[Deck]):
        super().__init__()
        self.window_title = "Browse Cards"
        self.layout = QHBoxLayout()
        # layout: filter list, card list, card edit
        self.filter_list_widget = QListWidget()
        self.layout.add_widget(self.filter_list_widget)

        self.card_list_widget = QListWidget()
        for deck in app_decks:
            for card in deck.cards:
                item = QListWidgetItem(f"{card.question} : {card.answer}")
                item.set_data(Qt.UserRole, card)
                self.card_list_widget.add_item(item)
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
        self.layout.add_widget(self.card_edit_widget)
