# Imports...

from tkinter import *

# Prevents unwanted windows
from functools import partial

import random
import pandas as pd

# Helper functions...

# Generates an anagram
def scramble(text):
    # create list of random characters from the string
    scramble_list = random.sample(text, len(text))

    # Join as a new string
    scrambled_text = "".join(scramble_list)
    return scrambled_text


# Collects terms and definitions and
# pairs them in a dictionary
def columns_to_dict(terms, definitions):
    '''
    Extracts the content from both columns in
    the csv file and returns them as a dictionary
    '''

    # Check that both columns are of the same degree
    if len(terms) != len(definitions):
        return {}
    else:
        return dict(zip(terms,definitions))


# Generates an anagram dictionary
# based on the number of rounds
def anag_generate(rounds):

    # Read the file
    excel_file = "science_vocab.XLSX"
    data_frame = pd.read_excel(excel_file)

    # Convert to csv
    csv_file = "science_vocab.csv"
    data_frame.to_csv(csv_file, index=False)

    # Extracting the terms and definitions
    terms = data_frame["Word"].tolist()
    definitions = data_frame["Definition"].tolist()

    i = 0

    # Remove the rest of the terms
    # and definitions in the list
    terms = terms[-rounds:]
    definitions = definitions[-rounds:]

    # Generate anagrams iteratively
    while i <= rounds-1:
        terms[i] = scramble(terms[i])
        i += 1

    # Create the dictionary
    vocab_dict = columns_to_dict(terms, definitions)

    return terms,vocab_dict


# Classes...
class Play:
    '''
    Interface for playing the quiz
    '''

    def __init__(self, rounds, difficulty):

        # Stats variables...
        self.correct_answers = 0
        self.skipped = 0

        self.words_guessed = []

        # Create the dictionary along
        # with the list of anagrams
        terms, vocab_dict = anag_generate(rounds)

        # Interface creation...
        self.quiz_frame = Frame(padx=10, pady=10)
        self.quiz_frame.grid()

        # String that holds the anagram
        anagram = random.choice(terms)
        print(anagram)


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("SciScramble")

    # Set number of rounds and difficulty
    # for demonstration purposes
    rounds = 5
    difficulty = "easy"
    Play(rounds,difficulty)
    root.mainloop()