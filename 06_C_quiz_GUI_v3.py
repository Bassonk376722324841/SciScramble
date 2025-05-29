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

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # Create the dictionary along
        # with the list of anagrams
        true_terms, terms, vocab_dict = anag_generate(mode)

        # Interface creation...

        self.quiz_box = Toplevel()

        # Create frame for the quiz
        self.quiz_frame = Frame(self.quiz_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # Universal font
        body_font = ("Arial","12")

        # Colours
        # ........

        # List for label details (text | font | color | row)
        quiz_label_list = [["Round # of #", ("Arial", "16", "bold"), None, 0],
                           ["Your term is...", body_font, "#D5E8D4", 2],
                           ["|>TESTING<|", body_font, "#D5E8D4", 4]]

        # create labels in a loop
        play_labels_ref = []
        for item in quiz_label_list:
            self.new_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                   bg=item[2], wraplength=300, justify="left")
            self.new_label.grid(row=item[3], padx=10, pady=10)

            play_labels_ref.append(self.new_label)

        # Loop for each round
        for i in range(0,rounds):

            n = random.randint(0,len(terms)-11)

            # String that holds anagram
            anagram = terms[n]

            # |>- testing quiz -<|
            answer = input(f"\n\nYour term is... {anagram}\ndefinition: {vocab_dict[anagram]}"
                           f"\n\nPlease enter the term you think is being hidden\n~~~ ")

            if answer == true_terms[n].lower():
                cont = input("\n\nYour answer is correct! Wanna continue?\n~~~ ").lower()

                if cont[0] == "n":
                    break
                else:
                    pass
            else:
                cont = input(f"\n\nOops! --- The correct term was {true_terms[n]}, wanna try again?\n~~~ ")

                cont = input("\n\nYour answer is correct! Wanna continue?\n~~~ ")

                if cont[0] == "n":
                    break
                else:
                    pass


        # Quiz text labels...

        # Loop for label creation...

        # Entry box for solution...

        # Next button creation...


    # helper functions...


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