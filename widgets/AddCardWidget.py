from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QMessageBox
from PySide6.QtCore import Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

import utils
from models.Flashcard import Flashcard


class AddCardWidget(QWidget):
    """This class defines the widget that will be displayed when the user clicks the "Add Card" button."""

    def __init__(self, app_decks):
        """
        Initialize the AddCardWidget with a list of decks.
        :param app_decks: The list of decks to choose from, to add the card to
        """
        super().__init__()
        self.layout = QVBoxLayout()
        self.window_title = "Add Card"

        self.decks = app_decks
        self.deck_label = QLabel("Deck:")
        self.layout.add_widget(self.deck_label)
        self.deck_dropdown = QComboBox()
        self.deck_dropdown.add_items([deck.name for deck in self.decks])
        self.layout.add_widget(self.deck_dropdown)

        self.question_label = QLabel("Front:")
        self.layout.add_widget(self.question_label)
        self.question_input = QLineEdit()
        self.question_input.returnPressed.connect(self.add_card)
        self.layout.add_widget(self.question_input)

        self.answer_label = QLabel("Back:")
        self.layout.add_widget(self.answer_label)
        self.answer_input = QLineEdit()
        self.answer_input.returnPressed.connect(self.add_card)
        self.layout.add_widget(self.answer_input)

        self.tags_label = QLabel("Tags (seperate by spaces):")
        self.layout.add_widget(self.tags_label)
        self.tags_input = QLineEdit()
        self.tags_input.returnPressed.connect(self.add_card)
        self.layout.add_widget(self.tags_input)

        self.add_card_button = QPushButton("Add Card")
        self.add_card_button.tool_tip = "Shortcut: Enter"
        self.add_card_button.clicked.connect(self.add_card)
        self.layout.add_widget(self.add_card_button)

        utils.setup_shortcuts(self, shortcuts={
            "Esc": self.close
        })
        self.set_layout(self.layout)
        self.resize(400, 300)
        self.show()

    @Slot()
    def add_card(self):
        """This method adds a new card to the selected deck"""
        deck_name = self.deck_dropdown.current_text
        question = self.question_input.text
        if not question:
            error_msg = QMessageBox()
            error_msg.text = 'The "Front" field cannot be blank.'
            error_msg.icon = QMessageBox.Warning
            error_msg.standard_buttons = QMessageBox.Ok

            shortcut_exit = QShortcut(QKeySequence("Esc"), error_msg)
            shortcut_exit.activated.connect(error_msg.close)
            error_msg.exec_()
            return
        answer = self.answer_input.text
        tags = self.tags_input.text.split(' ')

        for deck in self.decks:
            if deck.name == deck_name:
                deck.append_card(Flashcard(question, answer, tags=tags))
                break
        self.close()
