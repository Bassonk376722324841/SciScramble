from tkinter import *

# Prevents unwanted windows
from functools import partial

class StartQuiz:
    '''
    Initial interface for quiz that asks users
    to choose the amount of playable rounds.
    '''

    def __init__(self):
        '''
        Gets number of rounds
        '''

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

        # Variable for storing string values
        v = StringVar(root, "1")

        # Create difficulty buttons and
        # add them to the reference list
        difficulty_button_ref = []

        # Dictionary to create difficulty options
        options = [["Easy", 5, 0],
                   ["Normal", 5, 1]
                   ]

        # Loop to create the buttons
        for item in options:
            make_button = Radiobutton(self.start_frame, text=item[0],
                                      variable=v, indicator=0,
                                      background="light blue", )
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


    def check_rounds(self):
        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to homr screen)
        self.choose_label.config(fg="#889988", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Please choose a whole number above 0 or below 203"
        second_error = "Please enter the amount of rounds as a number"
        has_errors = "no"

        # Checks if the amount to be converted is a number above absolute zero.
        try:
            rounds_wanted = int(rounds_wanted)
            if 0 < rounds_wanted <= 203:
                # Clear entry box and reset instruction label so that when
                # users play a new game, they don't see an error message.
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # Invoke Play class (and take across number of rounds)
                Start(rounds_wanted)

                # Hide root window (ie: hide rounds rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes2"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

        elif has_errors == "yes2":
            self.choose_label.config(text=second_error, fg="#990000",
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

        info_text = "An anagram refers to a word pr phrase that is formed by " \
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


class Start:
    '''
    Interface for playing the SciScramble quiz
    '''

    def __init__(self, rounds):
        pass


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("SciScramble")
    StartQuiz()
    root.mainloop()