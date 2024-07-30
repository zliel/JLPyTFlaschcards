import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QAction, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QCheckBox, QLabel, \
    QMenuBar
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import utils
from widgets.CardBrowserWidget import CardBrowserWidget
from widgets.DeckListWidget import DeckListWidget
from widgets.AddCardWidget import AddCardWidget
from widgets.AddDeckWidget import AddDeckWidget
from widgets.Toast import Toast
from widgets.SettingsDialog import SettingsDialog
from theme import blue_dark_palette, default_text_font, button_font

my_app = QApplication([])
my_app.set_palette(blue_dark_palette)
my_app.set_font(button_font, "QPushButton")

settings = utils.load_config("settings.ini")
app_decks = utils.load_decks_from_csv(settings.get("USER", "decks_directory", fallback="decks"))


class MainWindow(QWidget):
    """This class defines the main window of the application, which will house all other necessary widgets."""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setup_menu()
        self.toast = Toast(self)
        self.toast.hide()
        self.decks = app_decks
        self.no_decks_label = QLabel(
            'No decks found. Click "Add Deck" to create a new deck, or "Generate Default Decks" to generate decks for JLPT N5-N1.')
        self.no_decks_label.font = default_text_font
        self.no_decks_label.alignment = Qt.AlignCenter
        if not self.decks:
            self.layout.add_widget(self.no_decks_label)
        self.deck_list_widget = DeckListWidget(self.decks)
        self.layout.add_widget(self.deck_list_widget)
        if not self.decks:
            self.no_decks_label.show()
            self.deck_list_widget.hide()

        # After clicking an "Add card" button, the AddCardWidget will be displayed
        self.button_layout = QHBoxLayout()
        self.add_card_button = QPushButton("Add Card")
        self.add_card_button.tool_tip = "Shortcut: Ctrl+N"
        self.add_card_button.clicked.connect(self.show_add_card_widget)
        self.button_layout.add_widget(self.add_card_button)

        self.add_deck_button = QPushButton("Add Deck")
        self.add_deck_button.tool_tip = "Shortcut: Ctrl+D"
        self.add_deck_button.clicked.connect(self.show_add_deck_widget)
        self.button_layout.add_widget(self.add_deck_button)

        self.browse_cards_button = QPushButton("Browse Cards")
        self.browse_cards_button.tool_tip = "Shortcut: Ctrl+B"
        self.browse_cards_button.clicked.connect(self.show_card_browser_widget)
        self.button_layout.add_widget(self.browse_cards_button)

        self.save_button = QPushButton("Save")
        self.save_button.tool_tip = "Shortcut: Ctrl+S"
        self.save_button.clicked.connect(
            lambda: utils.save_decks_to_csv(app_decks, settings.get("USER", "decks_directory", fallback="decks")))
        self.button_layout.add_widget(self.save_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.tool_tip = "Shortcut: Alt+S"
        self.settings_button.clicked.connect(self.show_settings_dialog)
        self.button_layout.add_widget(self.settings_button)

        self.generate_default_decks_button = QPushButton("Generate Default Decks")
        self.generate_default_decks_button.clicked.connect(self.show_generation_dialog)
        self.generate_default_decks_button.tool_tip = "Generate default decks for JLPT N5-N1"
        self.button_layout.add_widget(self.generate_default_decks_button)

        self.layout.add_layout(self.button_layout)

        # Shortcuts are being overridden by the menu bar, so they are commented out unless a shortcut not present in the menu bar
        # is needed.
        # utils.setup_shortcuts(self, shortcuts={
        #     "Ctrl+S": lambda: utils.save_decks_to_csv(app_decks,
        #                                               settings.get("DEFAULT", "decks_directory", fallback="decks")),
        #     "Ctrl+N": self.show_add_card_widget,
        #     "Ctrl+D": self.show_add_deck_widget,
        #     "Ctrl+B": self.show_card_browser_widget,
        #     "Ctrl+Q": self.close,
        #     "Alt+S": self.show_settings_dialog
        # })

        self.set_layout(self.layout)

        self.window_title = "JLPyT Flashcards"
        self.resize(1200, 700)
        # self.palette = Qt.black

        self.show()


    def save(self):
        utils.save_decks_to_csv(app_decks, settings.get("USER", "decks_directory", fallback="decks"))
        self.toast.show_toast("Saved Successfully")

    def setup_menu(self):
        menu_bar = QMenuBar(self)

        # Each menu is a dictionary of actions, where the key is the action name and the value is a tuple of the action and its shortcut
        menu_map = {
            "File": {
                "Save": (
                    lambda: utils.save_decks_to_csv(app_decks,
                                                    settings.get("USER", "decks_directory", fallback="decks")),
                    "Ctrl+S"),
                "Settings": (self.show_settings_dialog, "Alt+S"),
                "Exit": (self.close, "Ctrl+Q")
            },
            "Edit": {
                "Add Card": (self.show_add_card_widget, "Ctrl+N"),
                "Add Deck": (self.show_add_deck_widget, "Ctrl+D"),
                "Browse Cards": (self.show_card_browser_widget, "Ctrl+B")
            },
            "View": {
                "Show Normal": (self.show_normal, "F9"),
                "Show Maximized": (self.show_maximized, "F10"),
                "Show Full Screen": (self.show_full_screen, "F11")
            },
            "Tools": {
                "Generate Default Decks": (self.show_generation_dialog, None)
            },
            "Help": {
                "About": (lambda: self.toast.show_toast("JLPyT Flashcards v1.0.0"), None)
            }
        }

        # Loop through the map and build each menu
        for menu_name, actions in menu_map.items():
            menu = menu_bar.add_menu(menu_name)
            for action_name, (action, shortcut) in actions.items():
                menu_action = QAction(action_name, self)
                menu_action.triggered.connect(action)
                if shortcut:
                    menu_action.shortcut = shortcut
                menu.add_action(menu_action)

        self.layout.set_menu_bar(menu_bar)

    @Slot()
    def show_add_card_widget(self):
        """This method displays the AddCardWidget when the "Add Card" button is clicked."""
        add_card_widget = AddCardWidget(self.decks)
        add_card_widget.signals.card_added.connect(lambda: self.toast.show_toast("Card added!"))

    @Slot()
    def show_add_deck_widget(self):
        """ This method displays the AddDeckWidget when the "Add Deck" button is clicked. """
        add_deck_widget = AddDeckWidget(self.deck_list_widget)
        add_deck_widget.signals.deck_added.connect(self.reset_deck_list)
        add_deck_widget.signals.deck_added.connect(lambda: utils.save_decks_to_csv(app_decks, "decks"))
        add_deck_widget.signals.deck_added.connect(lambda: self.toast.show_toast("Deck added!"))

    @Slot()
    def show_card_browser_widget(self):
        """ This method displays the CardBrowserWidget when the "Browse Cards" button is clicked. """
        card_browser_widget = CardBrowserWidget(self.decks)
        card_browser_widget.signals.closed.connect(self.reset_deck_list)
        card_browser_widget.signals.closed.connect(lambda: utils.save_decks_to_csv(app_decks, "decks"))

    def reset_deck_list(self):
        """ This method resets the deck list widget after a new deck has been added. """
        if self.decks and self.no_decks_label.visible:
            self.no_decks_label.hide()
        elif not self.decks and not self.no_decks_label.visible:
            self.no_decks_label.show()
        new_deck_list_widget = DeckListWidget(self.decks)
        self.layout.replace_widget(self.deck_list_widget, new_deck_list_widget)
        self.deck_list_widget.delete_later()
        self.deck_list_widget = new_deck_list_widget

    @Slot()
    def show_generation_dialog(self):
        """ This method generates default decks for JLPT N5-N1. """
        # make a dialog box to ask the user which decks they want to generate
        generate_decks_dialog = QDialog()
        generate_decks_dialog.window_title = "Generate Default Decks"
        generate_decks_dialog.layout = QVBoxLayout()

        dialog_label = QLabel(
            "Select the decks you would like to generate (note that it will overwrite existing decks):")
        dialog_label.font = QFont("Arial", 12)
        generate_decks_dialog.layout.add_widget(dialog_label)

        default_deck_name_list = ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]
        check_box_list = []
        for deck_name in default_deck_name_list:
            check_box = QCheckBox(deck_name)
            check_box.checked = True
            check_box_list.append(check_box)
            generate_decks_dialog.layout.add_widget(check_box)

        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(
            lambda: self.generate_selected_decks(check_box_list, dialog=generate_decks_dialog))
        generate_decks_dialog.layout.add_widget(generate_button)
        generate_decks_dialog.set_layout(generate_decks_dialog.layout)
        generate_decks_dialog.resize(300, 200)
        generate_decks_dialog.exec()

    def generate_selected_decks(self, check_box_list, dialog):
        """ This method generates the selected decks. """
        dialog.find_child(QPushButton).text = "Downloading..."
        for check_box in check_box_list:
            level = int(check_box.text[-1])
            if check_box.checked:
                utils.download_deck_from_url(f"https://jlpt-vocab-api.vercel.app/api/words/all?level={level}",
                                             f"{check_box.text} Vocab",
                                             settings.get("USER", "decks_directory", fallback="decks"))

        print([deck.name for deck in self.decks])
        self.decks = utils.load_decks_from_csv(settings.get("USER", "decks_directory", fallback="decks"))
        self.reset_deck_list()
        self.toast.show_toast("Decks generated!")
        dialog.delete_later()

    @Slot()
    def show_settings_dialog(self):
        """ This method displays the settings widget. """
        settings_dialog = SettingsDialog(settings)
        settings_dialog.exec()


main_window = MainWindow()
main_window.show()

my_app.aboutToQuit.connect(lambda: utils.save_decks_to_csv(app_decks, "decks"))

sys.exit(my_app.exec())
