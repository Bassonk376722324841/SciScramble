from tkinter import *

class Stats:
    '''
    Interface for showing users the
    amount of rounds they won along
    with the words they found.
    '''

    def __init__(self, guesses, correct, skipped):
        self.stats_window = Toplevel()
        self.stats_window.title("Your Stats")

       # Label creation (soon to be improved for efficiency)
        Label(self.stats_window, text="Game Over!", font=("Arial", 16, "bold")).pack(pady=10)
        Label(self.stats_window, text=f"Correct Answers: {correct}").pack()
        Label(self.stats_window, text=f"Skipped: {skipped}").pack()
        Label(self.stats_window, text=f"Guessed Terms: {', '.join(guesses) if guesses else 'None'}",
              wraplength=300).pack(pady=10)

        Button(self.stats_window, text="Close", command=self.stats_window.destroy).pack(pady=5)


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