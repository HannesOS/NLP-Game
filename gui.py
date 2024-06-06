import numpy as np
import warnings; warnings.filterwarnings("ignore")
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Guess the word")
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        # Set up the main window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1800
        window_height = 900
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_widgets(self):
        # Define custom fonts and colors
        self.custom_font = ("Arial", 13)
        self.custom_font_big = ("Arial", 15)
        self.bg_color = "#375643"
        self.field_color = "#7d8d7c"
        self.button_color = "#607671"
        self.button_hover_color = "#7d8d7c"
        self.button_text_color = "#b8dbc2"
        self.button_hover_text_color = "#b8dbc2"
        self.font_color = "#b8dbc2"

        # Create frame for the 3D plot
        self.plot_frame = tk.Frame(self.root, bg=self.bg_color)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.plot_frame.config(highlightbackground="black", highlightthickness=0)
        self.plot_frame.pack_propagate(0)

        # Create 3D plot
        self.fig = plt.figure(figsize=(6, 6), facecolor=self.bg_color)
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.bg_color)

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot_canvas.mpl_connect("scroll_event", self.on_plot_scroll)
        self.initiate_plot()

        # Create frame for buttons and input/output
        self.control_frame = tk.Frame(self.root, bg=self.bg_color, width=600)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, anchor=tk.CENTER)
        self.control_frame.config(highlightbackground="black", highlightthickness=0)
        self.control_frame.pack_propagate(0)

        # Create buttons
        self.create_buttons()

        # Create string input
        self.create_input_output()

        # Create scrollable list
        self.create_scrollable_list()

    def create_buttons(self):
        # Create hint buttons and reset button
        self.button_hint = self.create_button(self.control_frame, "Hint", self.hint_action, 0, 0)
        self.button_strong_hint = self.create_button(self.control_frame, "Strong Hint", self.strong_hint_action, 0, 1, pady=15)
        self.button_reset_game = self.create_button(self.control_frame, "Reset", self.reset_game_action, 0, 2, pady=15)

        # Bind hover events to buttons
        self.bind_button_hover(self.button_hint)
        self.bind_button_hover(self.button_strong_hint)
        self.bind_button_hover(self.button_reset_game)

    def create_button(self, frame, text, command, row, column, pady=0):
        # Helper function to create buttons
        button = tk.Button(frame, text=text, command=command, width=20, height=2, bd=4,
                           bg=self.button_color, fg=self.button_text_color,
                           font=self.custom_font_big, highlightbackground="black",
                           highlightthickness=2, activebackground=self.button_hover_color,
                           activeforeground=self.button_hover_text_color)
        button.grid(row=row, column=column, padx=2, pady=pady)
        return button

    def bind_button_hover(self, button):
        # Bind hover events for button color change
        button.bind("<Enter>", self.on_enter_button)
        button.bind("<Leave>", self.on_leave_button)

    def create_input_output(self):
        # Create input label and entry
        self.input_label = tk.Label(self.control_frame, text="Input:", font=self.custom_font_big, bg=self.bg_color, fg=self.font_color)
        self.input_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.input_entry = tk.Entry(self.control_frame, font=self.custom_font_big, bg=self.field_color,
                                    highlightbackground="black", highlightthickness=2)
        self.input_entry.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        self.input_entry.bind("<Return>", self.guess_action)  # Bind Enter key event

        # Create output label and text box
        self.output_label = tk.Label(self.control_frame, text="Output:", font=self.custom_font_big, bg=self.bg_color, fg=self.font_color)
        self.output_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        self.output_text = tk.Text(self.control_frame, height=9, font=self.custom_font, bg=self.field_color,
                                   highlightbackground="black", highlightthickness=2, state='disabled')
        self.output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)

    def create_scrollable_list(self):
        # Create a scrollable list for guessed words
        self.scrollable_frame = tk.Frame(self.root, bg=self.bg_color)
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox_label = tk.Label(self.scrollable_frame, text="Guessed Words", bg=self.bg_color, font=self.custom_font_big, fg=self.font_color)
        self.listbox_label.pack(side=tk.TOP, fill=tk.X)
        self.listbox = tk.Listbox(self.scrollable_frame, highlightbackground="black", highlightthickness=2,
                                  selectbackground="black", bg=self.field_color, selectforeground="black",
                                  bd=0, relief=tk.FLAT, font=self.custom_font)
        self.listbox.bind("<MouseWheel>", self.listbox_on_mouse_wheel)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

    def initiate_plot(self):
        # Initialize the 3D plot
        self.ax.clear()
        self.ax.dist = 8
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.set_xlim([-1.1, 1.1])
        self.ax.set_ylim([-1.1, 1.1])
        self.ax.set_zlim([-1.1, 1.1])
        self.ax.scatter(self.game.embed_projection_word_to_guess[0], self.game.embed_projection_word_to_guess[1],
                        self.game.embed_projection_word_to_guess[2], vmin=0, vmax=1000, color="black", s=400, marker='X')
        self.plot_canvas.draw()

    def win_game(self):
        # Disable inputs and buttons when game is won
        self.input_entry.config(state='readonly')
        self.button_hint.config(state='disabled')
        self.button_strong_hint.config(state='disabled')
        self.button_reset_game.config(text='>>>Reset<<<')

    def on_enter_button(self, event):
        # Change button color on hover
        event.widget.config(bg=self.button_hover_color, fg=self.button_hover_text_color)

    def on_leave_button(self, event):
        # Revert button color when not hovered
        event.widget.config(bg=self.button_color, fg=self.button_text_color)

    def hint_action(self):
        # Provide a hint by guessing a word with a higher rank
        rank = int(self.game.best_word_rank * 0.9)
        hint = self.game.sorted_words[rank]
        self.guess_word(hint)

    def strong_hint_action(self):
        # Provide a stronger hint by guessing a word with a lower rank
        rank = int(self.game.best_word_rank * 0.3)
        hint = self.game.sorted_words[rank]
        self.guess_word(hint)

    def reset_game_action(self):
        # Reset the game and update the GUI
        self.game.reset_game()
        self.initiate_plot()
        self.listbox.delete(0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.input_entry.config(state='normal')
        self.button_hint.config(state='normal')
        self.button_strong_hint.config(state='normal')
        self.button_reset_game.config(text='Reset')
        self.write_to_output("Game reset. Make a new guess!")

    def guess_action(self, event):
        # Handle the guess input
        input_word = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.guess_word(input_word)

    def guess_word(self, word):
        # Process the guessed word and update the GUI
        output_message = self.game.handle_guess(word)
        if self.game.game_won:
            self.win_game()
        self.write_to_output(output_message)
        if self.game.current_word_rank >= 0:
            self.update_listbox(word)
            self.update_plot(word)

    def update_plot(self, input_word):
        # Update the 3D plot with the guessed word
        embed_projection = self.game.lower_dim_embed[np.argwhere(self.game.vocabulary == input_word)][0][0]
        self.ax.scatter(embed_projection[0], embed_projection[1], embed_projection[2], c=self.game.current_word_rank, vmin=0, vmax=1000, s=80, cmap='jet_r')
        self.ax.text(embed_projection[0]+0.02, embed_projection[1]+0.02, embed_projection[2]+0.02, f"{self.game.number_of_guesses}", size=15)
        self.plot_canvas.draw()

    def listbox_on_mouse_wheel(self, event):
        # Scroll the listbox with the mouse wheel
        self.listbox.yview_scroll(-1 * (event.delta // 120), "units")

    def on_plot_scroll(self, event):
        # Zoom in/out on the plot
        if event.button == "up":
            self.ax.dist -= 0.5
        elif event.button == "down":
            self.ax.dist += 0.5
        self.plot_canvas.draw()

    def update_listbox(self, word):
        # Update the scrollable list with the guessed word
        self.listbox.insert(tk.END, f"{self.game.number_of_guesses} {word}")
        self.listbox.yview_moveto(1)

    def write_to_output(self, text):
        # Write messages to the output text box
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.config(state="disabled")
        self.output_text.yview_moveto(1)