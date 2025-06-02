from tkinter import *

class Stats:
    '''
    Interface for showing users the
    amount of rounds they won along
    with the words they found.
    '''

    def __init__(self,rounds_won):
        pass


# Main routine
# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("SciScramble")

    # Set number of rounds won
    # for demonstration purposes
    rounds_won = 5
    Stats(rounds_won)
    root.mainloop()