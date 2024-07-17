import os
import re
import csv
import requests

from typing import List

from models.Deck import Deck
from models.Flashcard import Flashcard


def is_valid_filename(filename: str) -> bool:
    """
    Check if a filename is valid. A valid filename can only include alphanumeric characters, dashes, and hyphens, and
    must end with .csv
    :param filename: The filename to check
    :return: True if the filename is valid, False otherwise
    """
    # Filename can only include alphanumeric characters, dashes, and hyphens, and must end with .csv
    return re.match(r'^[\w\s-]+\.csv$', filename) is not None


def is_valid_path(basedir, path, follow_symlinks=True):
    """
    Check if a path is valid based on a base directory and whether to follow symlinks.
    A path is considered valid if it is a subdirectory of the base directory and, if follow_symlinks is False, the path
    is not a symlink.
    :param basedir: The base directory to check against
    :param path: The path to check
    :param follow_symlinks: Whether to follow symlinks, like shortcuts
    :return: True if the path is valid, False otherwise
    """
    if follow_symlinks:
        abs_path = os.path.abspath(path)
    else:
        abs_path = os.path.realpath(path)

    basedir = os.path.abspath(basedir)

    # Ensure the abs_path starts with basedir and that the next character is a path separator
    return abs_path.startswith(os.path.join(basedir, ''))


def save_deck_to_csv(deck: Deck, directory: str) -> None:
    """
    Save a deck to a CSV file in the specified directory
    :param deck: The deck to save, should be an instance of Deck and include Flashcard instances
    :param directory: The directory to save the deck to
    :return: None
    """
    if not deck.is_modified:
        print(f"Deck {deck.name} has not been modified")
        return  # Skip saving if the deck hasn't been modified

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{deck.name}.csv"
    print(f"Saving deck to {filename}")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Deck ID', 'Deck Name', 'Card ID', 'Question', 'Answer', 'Next Review Date', 'Repetitions',
                         'Easiness Factor', 'Interval', 'Tags'])
        for card in deck.cards:
            writer.writerow(
                [deck.id, deck.name, card.id, card.question, card.answer, card.next_review_date, card.repetitions,
                    card.easiness_factor, card.interval, card.tags])
    deck.is_modified = False  # Reset the modified flag after saving


def save_decks_to_csv(decks: List[Deck], directory: str) -> None:
    """
    Save a list of decks to CSV files in the specified directory
    :param decks: The list of decks to save
    :param directory: The directory to save the decks to, will be validated by is_valid_path
    :return: None
    """
    for deck in decks:
        save_deck_to_csv(deck, directory)


def load_deck_from_csv(filename: str) -> Deck:
    """
    Load a deck from a CSV file
    :param filename: The filename to load the deck from, including the directory
    :return: A Deck instance with the cards loaded from the CSV file
    """
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        cards = []
        deck_name = filename.split('\\')[-1].split('.')[0]
        print(f"Loading deck {deck_name}")
        for row in reader:
            card = Flashcard(
                question=row['Question'],
                answer=row['Answer'],
                next_review_date=row['Next Review Date'],
                repetitions=int(row['Repetitions']),
                easiness_factor=float(row['Easiness Factor']),
                interval=int(row['Interval']),
                id=row['Card ID'],
                tags=row['Tags']
            )
            cards.append(card)
        deck = Deck(name=deck_name, cards=cards)
        return deck


def load_decks_from_csv(directory: str) -> List[Deck]:
    """
    Load all decks from a directory
    :param directory: The directory to load the decks from, will be validated by is_valid_path
    :return: A list of Deck instances with the cards loaded from the CSV files
    """
    decks = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if is_valid_path(directory, filepath) and is_valid_filename(filename):
            deck = load_deck_from_csv(filepath)
            deck.is_modified = False
            decks.append(deck)
    return decks


# TODO: Consider making this more generic so it could be used with other APIs
def download_deck_from_url(url: str, deck_name: str, directory: str) -> None:
    """
    Download a deck from a URL and save it to a directory. Note that this was written for a specific API, located at https://jlpt-vocab-api.vercel.app and may need
    to be modified for other APIs.
    :param url: The URL to download the deck from
    :param deck_name: The name of the deck
    :param directory: The directory to save the deck to
    :return: None
    """
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()

        cards = []
        for card in response:
            front = card["word"]
            furigana = card["furigana"] + ' - ' if card["furigana"] != '' else ''
            back = furigana + card["meaning"]
            tags = [f'N{card["level"]}']

            new_card = Flashcard(front, back, tags=tags)
            cards.append(new_card)

        deck = Deck(deck_name, cards)
        save_deck_to_csv(deck, directory)
    else:
        print(f"Failed to download deck from {url}")
