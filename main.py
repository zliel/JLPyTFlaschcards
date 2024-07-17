import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import utils
from models.Deck import Deck
from models.Flashcard import Flashcard
from widgets.DeckListWidget import DeckListWidget

my_app = QApplication([])
label_font = QFont()
label_font.set_family("Times New Roman")
label_font.set_point_size(24)
my_app.set_font(label_font, "QLabel")

app_decks = utils.load_decks_from_csv("decks")

# If the user doesn't have any decks
if not app_decks:
    for i in range(1, 6):
        utils.download_deck_from_url(f"https://jlpt-vocab-api.vercel.app/api/words/all?level={i}", f"JLPT N{i} Vocab", "decks")

    app_decks = utils.load_decks_from_csv("decks")


class MainWindow(QWidget):
    """This class defines the main window of the application, which will house all other necessary widgets."""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.decks = app_decks
        self.deck_list_widget = DeckListWidget(self.decks)
        self.layout.add_widget(self.deck_list_widget)

        # After clicking a "Add card" button, the AddCardWidget will be displayed
        self.add_card_button = QPushButton("Add Card")
        self.add_card_button.clicked.connect(self.show_add_card_widget)
        self.layout.add_widget(self.add_card_button)

        self.add_deck_button = QPushButton("Add Deck")
        self.add_deck_button.clicked.connect(self.show_add_deck_widget)
        self.layout.add_widget(self.add_deck_button)

        self.set_layout(self.layout)

        self.window_title = "JLPyT Flashcards"
        self.resize(1200, 700)
        self.palette = Qt.black

        self.show()

    @Slot()
    def show_add_card_widget(self):
        """This method displays the AddCardWidget when the "Add Card" button is clicked."""
        from widgets.AddCardWidget import AddCardWidget
        add_card_widget = AddCardWidget(self.decks)


    @Slot()
    def show_add_deck_widget(self):
        """ This method displays the AddDeckWidget when the "Add Deck" button is clicked. """
        from widgets.AddDeckWidget import AddDeckWidget
        add_deck_widget = AddDeckWidget(self.deck_list_widget)
        add_deck_widget.signals.deck_added.connect(self.reset_deck_list)

    def reset_deck_list(self):
        """ This method resets the deck list widget after a new deck has been added. """
        new_deck_list_widget = DeckListWidget(self.decks)
        self.layout.replace_widget(self.deck_list_widget, new_deck_list_widget)
        self.deck_list_widget.delete_later()
        self.deck_list_widget = new_deck_list_widget




main_window = MainWindow()
main_window.show()

my_app.aboutToQuit.connect(lambda: utils.save_decks_to_csv(app_decks, "decks"))

sys.exit(my_app.exec())
