# Imports...

from tkinter import *

# Prevents unwanted windows
from functools import partial

import random
import pandas as pd


# Helper functions...

# Generates an anagram using two separate
# modes (example):
def scramble(text, mode):
    # create list of random characters from the string
    # based on the set difficulty

    if mode == "normal":

        # Create a completely random list of characters
        # from the given string
        scramble_list = random.sample(text, len(text))

        # Join as a new string
        scrambled_text = "".join(scramble_list)

    elif mode == "easy":

        # Create a random list with the first and last
        # characters of the characters being the same

        inner_len = len(text) - 1

        scramble_list = random.sample(text[1:inner_len], len(text[1:inner_len]))

        # Join as a new string with first
        # and last characters kept the same
        scrambled_text = "".join(scramble_list)

        scrambled_text = text[0] + scrambled_text + text[-1]

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
def anag_generate(mode):

    # Read the file
    excel_file = "science_vocab.XLSX"
    data_frame = pd.read_excel(excel_file)

    # Convert to csv
    csv_file = "science_vocab.csv"
    data_frame.to_csv(csv_file, index=False)

    # Extracting the terms and definitions
    terms = data_frame["Word"].tolist()

    # Make a copy of the terms for anagrams
    terms_anag = []

    definitions = data_frame["Definition"].tolist()

    for i, term in enumerate(terms):
        terms_anag.append(scramble(terms[i],mode))

    # Create the dictionary
    vocab_dict = columns_to_dict(terms_anag, definitions)

    return terms, terms_anag, vocab_dict


# Classes...
class Play:
    '''
    Interface for playing the quiz
    '''

    def __init__(self, rounds, mode):

        # Stats variables...
        self.correct_answers = IntVar()
        self.skipped = 0

        self.words_guessed = []

        # Round variables for iterative
        # tracking of results
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # Index to show number of rounds
        self.round_idx = 1

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # Create the dictionary along
        # with the list of anagrams
        true_terms, terms, vocab_dict = anag_generate(mode)

        # Interface creation...

        # Create frame for the quiz
        self.quiz_frame = Frame(padx=10, pady=10)
        self.quiz_frame.grid()

        # Universal font
        body_font = ("Arial","12")

        n = random.randint(0, len(terms) - 11)

        # String that holds anagram
        anagram = terms[n]

        # List for label details (text | font | color | row)
        quiz_label_list = [[f"Round {self.round_idx} of {rounds}", ("Arial", "16", "bold"), None, 0],
                           ["Your term is...", body_font, None, 2],
                           [anagram, body_font, "white", 4],
                           [f"Definition: {vocab_dict[anagram]}", ("Arial", "10", "bold"), None, 5]]

        # create labels in a loop
        quiz_labels_ref = []
        for item in quiz_label_list:
            self.new_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                   bg=item[2], wraplength=300, justify="left")
            self.new_label.grid(row=item[3], padx=10, pady=10)

            quiz_labels_ref.append(self.new_label)

        # Add entry box

        # Frame for keeping entry button and entry box side by side
        self.entry_area_frame = Frame(self.quiz_frame)
        self.entry_area_frame.grid(row=6)

        self.term_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                          width=10)
        self.term_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...

        # Create play button
        self.continue_button = Button(self.entry_area_frame, font=("Arial", "12", "bold"),
                                       fg="#FFFFFF", bg="#0057D8", text="Next", width=10,
                                       command=self.check_play)
        self.continue_button.grid(row=0, column=1)

    def check_play(self):
        answer = self.term_entry.get()
        print(answer)


# Stat class...
class Stats:
    '''
    Interface for showing the player's
    stats at the end of the quiz
    '''

    def __init__(self):
        pass


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