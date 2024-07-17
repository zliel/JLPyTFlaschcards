from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, Slot, Signal, QObject

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
from widgets.DeckListWidget import DeckListWidget


class AddDeckWidgetSignals(QObject):
    deck_added = Signal()


class AddDeckWidget(QWidget):
    signals = AddDeckWidgetSignals()

    def __init__(self, deck_list_widget: DeckListWidget):
        super().__init__()
        self.window_title = "Add a deck"
        self.deck_list_widget = deck_list_widget
        self.layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.deck_name_label = QLabel("Deck Name:")
        form_layout.add_widget(self.deck_name_label)
        self.deck_name_input = QLineEdit()
        form_layout.add_widget(self.deck_name_input)
        self.layout.add_layout(form_layout)

        self.add_deck_button = QPushButton("Add Deck")
        self.add_deck_button.clicked.connect(self.add_deck)
        self.layout.add_widget(self.add_deck_button)

        self.set_layout(self.layout)
        self.resize(400, 300)
        self.show()

    @Slot()
    def add_deck(self):
        deck_name = self.deck_name_input.text
        self.deck_list_widget.decks.append(Deck(deck_name, []))

        self.signals.deck_added.emit()
        self.close()

