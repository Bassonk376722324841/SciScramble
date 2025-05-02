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

        # Create button for players that are not
        # aware of what anagrams arw
        self.anag_info_button = Button(self.start_frame, font=("Arial", "9", "bold"),
                                       fg="purple", text="What are anagrams?", width=17,
                                       command=self.open_info)
        self.anag_info_button.grid(row=3, column=0)


    def open_info(self):
        Info(self)


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
                                height=200,bg=background)
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


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("SciScramble")
    StartQuiz()
    root.mainloop()