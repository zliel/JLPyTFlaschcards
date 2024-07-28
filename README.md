# JLPyT Flashcards

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
This is a simple-to-use flashcard application that allows users to create, edit, and delete flashcards, which they can then review.
While this was originally created for the purpose of studying Japanese, it can be used for any subject. You can generate decks of vocabulary
for the JLPT N5, N4, N3, N2, and N1 levels, or create your own custom decks and cards. Thanks to [GitHub user Wkei](https://jlpt-vocab-api.vercel.app), whose API I used to generate the JLPT decks.
This application was created using Python and the PySide6 library, and uses the SM-2 algorithm to determine when to show cards for review.

## Installation
To install this application, you will need to have Python 3.6 or later installed on your computer. You can download the latest version of Python [here](https://www.python.org/downloads/).
Once you have Python installed, you can download the source code from this repository and run the following command in the root directory of the project to install the required dependencies:
```
pip install -r requirements.txt
```

Then, you can run the following command to start the application:
```
python main.py
```