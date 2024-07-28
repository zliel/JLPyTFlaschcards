# JLPyT Flashcards

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

### Introduction
This is a simple-to-use flashcard application that allows users to create, edit, and delete flashcards, which they can then review.
While this was originally created for the purpose of studying Japanese, it can be used for any subject. You can generate decks of vocabulary
for the JLPT N5, N4, N3, N2, and N1 levels, or create your own custom decks and cards. Thanks to [GitHub user Wkei](https://jlpt-vocab-api.vercel.app), whose API I used to generate the JLPT decks.
This application was created using Python and the PySide6 library, and uses the SM-2 algorithm to determine when to show cards for review.

### Installation
To install this application, you will need to have Python 3.6 or later installed on your computer. You can download the latest version of Python [here](https://www.python.org/downloads/).
Once you have Python installed, you can download the source code from this repository and run the following command in the root directory of the project to install the required dependencies:
```
pip install -r requirements.txt
```

Then, you can run the following command to start the application:
```
python main.py
```

### Usage
#### Getting Started
<hr>
When you first start the application, you will see the main window with a notice that you have no decks to review. You can either add your own decks, or generate default ones for JLPT N5-N1 using the "Generate Default Decks" button.
To create a new deck, click the "Add Deck" button and enter a name for the deck. You can then add new cards to the deck by clicking the "Add Card" button.

#### Reviewing Cards
<hr>
To review cards, click the "View Deck" button next to the deck you want to review. You will see a card with a question on the front and an answer on the back. You can flip the card by clicking on it, and you can mark the card as "Pass" or "Fail" by clicking the corresponding button. 
The card will be shown again in the future based on your response. 

#### The Browser
<hr>
You can view all of your cards by close the "Browse Cards" button, and you can edit cards by selecting them, after which the card editor will show. You can save changes to a card with the "Save" button at the bottom of the editor.
You can delete a card by selecting it in the browser and pressing "Delete" on your keyboard. On the left of the browser, you'll see a list of filters,
including deck names and tags. You can filter cards by double-clicking on a filter, and you can remove a filter by selecting it and pressing the "Delete" key on your keyboard. 

#### Settings
<hr>
You can access the settings by clicking the "Settings" button in the main window. 
Here, you can change the number of new cards to learn each day, the number of review cards to show each day, where your decks are located/will be saved/loaded to, and you can select the application's theme.

#### How Decks are Stored
<hr>
Decks are stored in csv files in the deck_directory specified in the settings ("decks" by default). Each deck has its own csv file, and each card is a row in the file. The columns are as follows:
 - Deck ID (unique identifier for each deck, but every row in the deck needs this to be the same)
 - Deck Name
 - Card ID (unique identifier)
 - Question 
 - Answer
 - Next Review Date (ISO time format)
 - Repetitions (default is 0)
 - Easiness Factor (default is 2.5)
 - Interval (default is 0)
 - Tags
