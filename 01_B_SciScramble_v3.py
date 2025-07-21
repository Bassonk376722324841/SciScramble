# Imports...

from tkinter import *

# Prevents unwanted windows
from functools import partial

import random
import pandas as pd


# Prevents unwanted windows
from functools import partial

# Helper functions...

# Generates an anagram using two separate
# modes (example):
def scramble(text, mode):
    # create list of random characters from the string
    # based on the set difficulty

    if mode == "Normal":

        print(text)

        # Create a completely random list of characters
        # from the given string
        scramble_list = random.sample(text, len(text))

        # Join as a new string
        scrambled_text = "".join(scramble_list)

    elif mode == "Easy":

        # Create a random list with the first and last
        # characters of the characters being the same

        inner_len = len(text) - 1

        scramble_list = random.sample(text[1:inner_len], len(text[1:inner_len]))

        # Join as a new string with first
        # and last characters kept the same
        scrambled_text = text[0] + "".join(scramble_list) + text[-1]

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


# Classes...

class StartQuiz:
    '''
    Initial interface for quiz that asks users
    to choose the amount of playable rounds.
    '''

    def __init__(self):
        '''
        Gets number of rounds
        '''

       # <--- Extracting terms --->

        # Read the file
        excel_file = "science_vocab.XLSX"
        data_frame = pd.read_excel(excel_file)

        # Extracting the terms and definitions
        self.terms = data_frame["Word"].tolist()

        self.definitions = data_frame["Definition"].tolist()

        self.vocab_dict = columns_to_dict(self.terms, self.definitions)

        # <--- Rest of program --->

        # Set the initial game mode to
        # a blank string
        self.mode = ""

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("In each round you will be challenged to enter what word "
                        "you believe is being shown in an  anagram and learn new "
                        "scientific terms with each success!")

        round_string = "Choose number of rounds"

        # List of labels to be made (text | font | fg) | row
        start_labels_list = [
            ["SciScramble", ("Arial", "16", "bold"), None, 0],
            [intro_string, ("Arial", "12"), None, 1],
            [round_string, ("Arial", "11", "bold"), "grey", 3],
            ["difficulty:", ("Arial", "11", "bold"), "grey", 4]
        ]

        # Create labels and add them to the reference list
        start_label_ref = []

        # Loop to create multiple labels
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=350, justify="left", padx=20, pady=10)
            make_label.grid(row=item[3])

            start_label_ref.append(make_label)

        # Create button for players that are not
        # aware of what anagrams arw
        self.anag_info_button = Button(self.start_frame, font=("Arial", "9", "bold"),
                                       fg="purple", text="What are anagrams?", width=17,
                                       command=self.open_info)
        self.anag_info_button.grid(row=2, column=0)

        # Creating difficulty buttons...

        # Create difficulty buttons and
        # add them to the reference list
        difficulty_button_ref = []

        # Dictionary to create difficulty options
        options = [["Easy", 0, 0],
                   ["Normal", 0, 1]
                   ]

        # Initialize difficulty selection frame
        self.dif_frame = Frame(self.start_frame)
        self.dif_frame.grid(row=5)

        # Loop to create the buttons
        for item in options:
            make_button = Button(self.dif_frame, text=item[0],
                                      background="light blue",
                                      command=lambda mode=item[0]: self.button_check(mode))
            make_button.grid(row=item[1], column=item[2])

            difficulty_button_ref.append(make_button)

        # Extract choice label so that it can be
        # replaced with an error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that an entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=6)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)


    def open_info(self):
        Info(self)


    def button_check(self,mode):
        self.mode = mode


    def check_rounds(self):
        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to homr screen)
        self.choose_label.config(fg="#889988", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        # Set of possible errors a user can get
        error = "Please choose a whole number above 0 or below 204"
        second_error = "Please enter the amount of rounds as a number"
        has_errors = "no"

        # An error given for when a game
        # difficulty isn't chosen
        diff_error = ""

        # Checks if the number of rounds is within the range of 1 and 203
        # and if the difficulty has been chosen
        try:
            rounds_wanted = int(rounds_wanted)

            if 0 < rounds_wanted <= 203 and self.mode != "":
                # Clear entry box and reset instruction label so that when
                # users start over, or they don't see an error message.
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # Invoke Play class (and take across number of rounds)
                Play(rounds_wanted,self.mode, self.terms, self.vocab_dict)

                # Hide root window (ie: hide rounds rounds choice window)
                root.withdraw()

            elif rounds_wanted < 0 or rounds_wanted > 203:
                has_errors = "yes"
            elif self.mode == "":
                has_errors = "yes3"
        except ValueError:
            has_errors = "yes2"

        # Managing difficulty selection errors
        if self.mode == "" and has_errors != "no":
            diff_error = ", please choose the quiz difficulty"
        elif self.mode == "" and has_errors == "no":
            diff_error = "Please choose the quiz difficulty"

            # If nothing is wrong with the round input,
            # yet no difficulty is chosen, the 3rd error
            # type will be used.
            has_errors = "yes3"



        # Display the error if necessary
        if has_errors == "yes3":
            self.choose_label.config(text=diff_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

        elif has_errors == "yes2":
            self.choose_label.config(text=second_error+diff_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

        elif has_errors == "yes":
            self.choose_label.config(text=error + diff_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Info:
    '''
    Interface for explaining what anagrams are
    '''

    def __init__(self, partner):
        background = "beige"
        self.info_box = Toplevel()

        # If users press x at top, close help and
        # 'release' the help button
        self.info_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_info, partner))

        # Disable help button
        partner.anag_info_button.config(state=DISABLED)

        self.info_frame = Frame(self.info_box, width=300,
                                height=200, bg=background)
        self.info_frame.grid()

        self.info_heading_label = Label(self.info_frame,
                                        text="What are anagrams?",
                                        font=("Arial", "14", "bold"))
        self.info_heading_label.grid(row=0)

        info_text = "An anagram refers to a word or phrase that is formed by " \
                    "rearranging the characters of another one. The use of " \
                    "anagrams in SciScramble is to hide the word that is given " \
                    "each round. Once solved, a scientific term is revealed!\n\n" \
                    " You get a definition of the hidden word at the beginning " \
                    "(easy) or at the end (normal) of each round!"

        self.info_text_label = Label(self.info_frame,
                                     text=info_text, wraplength=350,
                                     justify="left")
        self.info_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.info_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", command=partial(self.close_info, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.info_frame, self.info_heading_label,
                         self.info_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_info(self, partner):
        '''
        Closes help dialogue box and enables help button
        '''

        partner.anag_info_button.config(state=NORMAL)
        self.info_box.destroy()


class Play:
    '''
    Interface for playing the quiz
    '''

    def __init__(self, rounds, mode, terms, vocab_dict):

        # Stats variables...
        self.correct_answers = 0
        self.skipped = 0

        # Save the terms, mode and dictionary
        self.terms = terms
        self.mode = mode
        self.vocab_dict = vocab_dict

        self.successful_guesses = []

        # Round variables for iterative
        # tracking of results
        self.rounds_played = 0

        # Binary variable that helps determine
        # whether a round has ended or not
        self.played = False

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # <--- Interface creation --->

        # Create frame for the quiz
        self.quiz_frame = Toplevel()
        self.quiz_frame.title("Your Stats")

        # Universal font
        body_font = ("Arial","12")

        # Generate a random number that gets
        # used for choosing a random anagram
        self.n = random.randint(0, len(terms) - 1)

        # String that holds anagram
        anagram = scramble(self.terms[self.n],self.mode)

        # List for label details (text | font | color | row)
        quiz_label_list = [[f"Round {self.rounds_played+1} of {rounds}", ("Arial", "16", "bold"), None, 0],
                           ["Your term is...", body_font, None, 2],
                           [f"{anagram}", body_font, "white", 4],
                           [f"Definition: {vocab_dict[terms[self.n]]}", ("Arial", "10", "bold"), None, 5]]

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

        # If the user has completed a round, move to the next one
        if self.played:

            # Set the success label back to its original state
            self.quiz_labels_ref[1].config(text="Your term is...")

            self.rounds_played += 1

            # Update heading label and anagram if the
            # player has already completed a round. Also
            # decides on whether to show stats or not
            if self.rounds_played >= rounds_wanted:

                # Disable the "Next" button once in stats view
                self.continue_button.config(text="+", state=DISABLED)
                self.skip_button.config(text="-", state=DISABLED)

                Stats(self.successful_guesses, self.correct_answers, self.skipped)
                return

            self.term_entry.delete(0, END)
            self.quiz_labels_ref[0].config(text=f"Round {self.rounds_played + 1} of {rounds_wanted}")

            self.n = random.randint(0, len(self.terms) - 1)
            anagram = scramble(self.terms[self.n],self.mode)

            self.quiz_labels_ref[2].config(text=anagram)
            self.quiz_labels_ref[3].config(text=f"Definition: {self.vocab_dict[self.terms[self.n]]}")

            self.skip_button.config(text="- S kip", state=ACTIVE)
            self.played = False
            return

        # If input is empty or added spaces
        if len(answer) == 0:
            self.quiz_labels_ref[1].config(text="Please enter text without open spaces")
            self.term_entry.delete(0, END)
            return

        # Compare user answer with actual answer
        if answer == self.terms[self.n].lower():
            self.term_entry.delete(0, END)
            self.quiz_labels_ref[1].config(text="You've got it!")
            self.correct_answers += 1
            self.successful_guesses.append(answer)
            self.skip_button.config(state=DISABLED)
            self.played = True

        # If the user enters the wrong answer
        else:
            self.term_entry.delete(0, END)
            self.quiz_labels_ref[1].config(text=f"Oops! The answer was {self.terms[self.n]}")
            self.skip_button.config(text="-", state=DISABLED)
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

        # text | font | pady
        labels = [
            ["You've went through all scrambles!", ("Arial",16,"bold"), 10],
            [f"Correct answers: {correct}",("Arial",13,"bold"), None],
            [f"Skipped: {skipped}", ("Arial",13,"bold"), None],
            [f"Guessed Terms:\n{','.join(guesses) if guesses else 'None'}", ("Arial",16,"bold"), None]
        ]

        for item in labels:
            new_label = Label(self.stats_window, text=item[0],font=item[1])
            new_label.grid()

        close_button = Button(self.stats_window, text="Close", command=self.stats_window.destroy)
        close_button.grid()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("SciScramble")
    StartQuiz()
    root.mainloop()