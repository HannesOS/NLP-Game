import tkinter as tk
from src.game import WordGuessingGame
from src.gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessingGame()
    gui = GUI(root, game)
    root.mainloop()