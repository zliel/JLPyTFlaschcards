from configparser import ConfigParser

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QDialog
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

import utils
from theme import default_text_font


class SettingsDialog(QDialog):
    def __init__(self, settings: ConfigParser):
        super().__init__()
        self.window_title = "Settings"
        self.settings = settings
        self.layout = QVBoxLayout()
        self.layout.alignment = Qt.AlignCenter

        review_layout = QHBoxLayout()
        self.review_limit_label = QLabel("Review Limit:")
        self.review_limit_label.font = default_text_font
        review_layout.add_widget(self.review_limit_label)
        self.review_limit_input = QLineEdit()
        self.review_limit_input.font = default_text_font
        self.review_limit_input.text = self.settings['USER']['daily_reviews_limit'] if 'USER' in self.settings.sections() else '100'
        only_int_validator = QIntValidator()
        only_int_validator.set_range(0, 1000)
        self.review_limit_input.set_validator(only_int_validator)
        review_layout.add_widget(self.review_limit_input)
        self.layout.add_layout(review_layout)

        new_cards_layout = QHBoxLayout()
        self.new_cards_limit_label = QLabel("New Cards Limit:")
        self.new_cards_limit_label.font = default_text_font
        new_cards_layout.add_widget(self.new_cards_limit_label)
        self.new_cards_limit_input = QLineEdit()
        self.new_cards_limit_input.font = default_text_font
        self.new_cards_limit_input.set_validator(only_int_validator)
        self.new_cards_limit_input.text = self.settings['USER']['new_card_limit'] if 'USER' in self.settings.sections() else '20'
        new_cards_layout.add_widget(self.new_cards_limit_input)
        self.layout.add_layout(new_cards_layout)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.add_widget(self.save_button)

        self.resize(300, 200)
        self.set_layout(self.layout)

    @Slot()
    def save_settings(self):
        # If the user section doesn't exist, it will be a copy of the default settings
        if 'USER' not in self.settings.sections():
            self.settings['USER'] = self.settings['DEFAULT']
        self.settings['USER']['daily_reviews_limit'] = self.review_limit_input.text
        self.settings['USER']['new_card_limit'] = self.new_cards_limit_input.text
        utils.save_config(self.settings, "settings.ini")
        self.close()
