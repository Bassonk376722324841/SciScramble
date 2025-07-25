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
        self.correct_answers = 0
        self.skipped = 0

        self.successful_guesses = []

        # Round variables for iterative
        # tracking of results
        self.rounds_played = 0

        # Binary variable that helps determine
        # whether a round has ended or not
        self.played = False

        # Determines whether to show a spacing
        # error at the beginning of the round
        self.beginning = True

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # Create the dictionary along
        # with the list of anagrams
        self.true_terms, self.terms, self.vocab_dict = anag_generate(mode)

        # Interface creation...

        # Create frame for the quiz
        self.quiz_frame = Frame(padx=15, pady=15)
        self.quiz_frame.grid()

        # Universal font
        body_font = ("Arial","12")

        self.n = random.randint(0, len(self.terms) - 1)

        # String that holds anagram
        anagram = self.terms[self.n]

        # List for label details (text | font | color | row)
        quiz_label_list = [[f"Round {self.rounds_played+1} of {rounds}", ("Arial", "16", "bold"), None, 0],
                           ["Your term is...", body_font, None, 2],
                           [anagram, body_font, "white", 4],
                           [f"Definition: {self.vocab_dict[anagram]}", ("Arial", "10", "bold"), None, 5]]

        # create labels in a loop
        self.quiz_labels_ref = []
        for item in quiz_label_list:
            self.new_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                   bg=item[2], wraplength=300, justify="left")
            self.new_label.grid(row=item[3], padx=10, pady=10)

            self.quiz_labels_ref.append(self.new_label)

        # Add entry box

        # Frame for keeping entry button and entry box side by side
        self.entry_area_frame = Frame(self.quiz_frame)
        self.entry_area_frame.grid(row=7)

        self.term_entry = Entry(self.quiz_frame, font=("Arial", "20", "bold"),
                                          width=10)
        self.term_entry.grid(row=6, column=0, padx=10, pady=10)

        # Create play button
        self.continue_button = Button(self.entry_area_frame, font=("Arial", "12", "bold"),
                                       fg="#FFFFFF", bg="#0057D8", text="N ext   +", width=10,
                                       command=self.new_round)
        self.continue_button.grid(row=1, column=1)

        # Create skip button
        self.skip_button = Button(self.entry_area_frame, font=("Arial", "12", "bold"),
                                  bg="red", fg="#FFFFFF", text="-   S kip", width=10,
                                  command=self.skip)
        self.skip_button.grid(row=1, column=0)


    def skip(self):

        # Skips the current round
        self.skipped += 1
        self.played = True
        self.new_round()

    def new_round(self):
        '''
        Compare the user answer with the actual answer
        and change records accordingly and
        continue to next round
        '''

        rounds_wanted = self.rounds_wanted.get()
        answer = self.term_entry.get().strip().lower()

        # End the game if all rounds are completed
        if self.rounds_played >= rounds_wanted:
            Stats(self.successful_guesses, self.correct_answers, self.skipped)
            return

        # If the user has completed a round, move to the next one
        if self.played:
            self.rounds_played += 1

            # Update heading label and anagram if the
            # player has already completed a round. Also
            # decides on whether to show stats or not
            if self.rounds_played >= rounds_wanted:
                Stats(self.successful_guesses, self.correct_answers, self.skipped)
                return

            self.term_entry.delete(0, END)
            self.quiz_labels_ref[0].config(text=f"Round {self.rounds_played + 1} of {rounds_wanted}")

            self.n = random.randint(0, len(self.terms) - 1)
            anagram = self.terms[self.n]

            self.quiz_labels_ref[2].config(text=anagram)
            self.quiz_labels_ref[3].config(text=f"Definition: {self.vocab_dict[anagram]}")

            self.skip_button.config(state=ACTIVE)
            self.played = False
            return

        # If input is empty or added spaces
        if len(answer) == 0:
            self.quiz_labels_ref[1].config(text="Please enter text without open spaces")
            self.term_entry.delete(0, END)
            return

        # Compare user answer with actual answer
        if answer == self.true_terms[self.n].lower():
            self.term_entry.delete(0, END)
            self.quiz_labels_ref[1].config(text="You've got it!")
            self.correct_answers += 1
            self.successful_guesses.append(answer)
            self.skip_button.config(state=DISABLED)
            self.played = True

        # If the user enters the wrong answer
        else:
            self.term_entry.delete(0, END)
            self.quiz_labels_ref[1].config(text=f"Oops! The answer was {self.true_terms[self.n]}")
            self.skip_button.config(state=DISABLED)
            self.played = True


# Stat class...
class Stats:
    '''
    Interface for showing the player's
    stats at the end of the quiz
    '''

    def __init__(self, guesses, correct, skipped):
        self.stats_window = Toplevel()
        self.stats_window.title("Your Stats")

        Label(self.stats_window, text="Game Over!", font=("Arial", 16, "bold")).pack(pady=10)
        Label(self.stats_window, text=f"Correct Answers: {correct}").pack()
        Label(self.stats_window, text=f"Skipped: {skipped}").pack()
        Label(self.stats_window, text=f"Guessed Terms:\n{', '.join(guesses) if guesses else 'None'}",
        wraplength=300).pack(pady=10)

        Button(self.stats_window, text="Close", command=self.stats_window.destroy).pack(pady=5)


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