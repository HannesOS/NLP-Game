import tkinter as tk
from game import WordGuessingGame
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessingGame()
    gui = GUI(root, game)
    root.mainloop()