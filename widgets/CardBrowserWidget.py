from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
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
        self.layout.add_widget(self.card_list_widget)

        self.card_edit_widget = None

        self.show()
