import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from models.Deck import Deck
from models.Flashcard import Flashcard
from widgets.DeckListWidget import DeckListWidget

my_app = QApplication([])
label_font = QFont()
label_font.set_family("Times New Roman")
label_font.set_point_size(24)
my_app.set_font(label_font, "QLabel")


# TODO: Remove this, it's for testing purposes
n5_animal_deck = Deck("JLPT N5 Animals", [
    Flashcard("犬", "いぬ - Dog"),
    Flashcard("猫", "ねこ - Cat"),
    Flashcard("鳥", "とり - Bird"),
    Flashcard("馬", "うま - Horse")
])


class MainWindow(QWidget):
    """This class defines the main window of the application, which will house all other necessary widgets."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        deck_list_widget = DeckListWidget([n5_animal_deck])
        self.layout.add_widget(deck_list_widget)

        self.set_layout(self.layout)


        self.window_title = "JLPyT Flashcards"
        self.resize(1200, 700)
        self.palette = Qt.black


main_window = MainWindow()
main_window.show()

sys.exit(my_app.exec())
