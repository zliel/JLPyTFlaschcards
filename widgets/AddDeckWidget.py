from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, Slot, Signal, QObject

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
from widgets.DeckListWidget import DeckListWidget


class AddDeckWidgetSignals(QObject):
    """
    This class defines the signals that is emitted when a deck is added.
    """
    deck_added = Signal()


class AddDeckWidget(QWidget):
    """
    This widget allows the user to add a new deck to the deck list widget.
    """
    signals = AddDeckWidgetSignals()

    def __init__(self, deck_list_widget: DeckListWidget):
        """
        Initialize the AddDeckWidget with the app's current DeckListWidget.
        :param deck_list_widget: The DeckListWidget to add the new deck to
        """
        super().__init__()
        self.window_title = "Add a deck"
        self.deck_list_widget = deck_list_widget
        self.layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.deck_name_label = QLabel("Deck Name:")
        form_layout.add_widget(self.deck_name_label)
        self.deck_name_input = QLineEdit()
        # Can't use "Enter" as a shortcut because of the way QLineEdit handles the "Enter" key, so we connect the
        # return_pressed signal to the add_deck method instead
        self.deck_name_input.returnPressed.connect(self.add_deck)
        form_layout.add_widget(self.deck_name_input)
        self.layout.add_layout(form_layout)

        self.add_deck_button = QPushButton("Add Deck")
        self.add_deck_button.clicked.connect(self.add_deck)
        self.layout.add_widget(self.add_deck_button)

        self.setup_shortcuts()
        self.set_layout(self.layout)
        self.resize(400, 300)
        self.show()

    @Slot()
    def add_deck(self):
        """ This method adds a new deck to the deck list widget """
        deck_name = self.deck_name_input.text
        self.deck_list_widget.decks.append(Deck(deck_name, []))

        self.signals.deck_added.emit()
        self.close()

    def setup_shortcuts(self):
        """ This method sets up the keyboard shortcuts for the AddDeckWidget """
        shortcuts = {
            "Esc": self.close
        }

        for key_sequence, action in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key_sequence), self)
            shortcut.activated.connect(action)
