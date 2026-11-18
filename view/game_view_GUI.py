import tkinter as tk

from model.player import player
from view.board_view import BoardView
from view.game_view import GameView


class GameClosed(Exception):
    """Stop the controller when the player closes the main window."""


class GameViewGUI(GameView):
    """Display player interactions in the same window as the board."""

    def __init__(self, board_view: BoardView, player: player, root: tk.Tk):
        super().__init__(board_view, player)
        self.root = root
        self.closed = False
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.lives_label = tk.Label(root)
        self.lives_label.grid(row=player.lives_start + 1, column=0, columnspan=2)

    def close(self):
        self.closed = True
        self.root.quit()

    def _wait(self):
        if not self.closed:
            self.root.mainloop()
        if self.closed:
            raise GameClosed()

    def display_lives(self):
        self.lives_label.configure(text=f'Lives:{self.player.lives_left}')

    def get_guess(self):
        guess_value = tk.StringVar(master=self.root)
        entry = tk.Entry(self.root, textvariable=guess_value, width=5)
        entry.grid(row=self.player.lives_start + 1, column=3, sticky='nsew')
        button = tk.Button(self.root, text='Guess', command=self.root.quit)
        button.grid(row=self.player.lives_start + 1, column=2, sticky='nsew')
        entry.bind('<Return>', lambda event: self.root.quit())
        entry.focus_set()
        try:
            self._wait()
            return guess_value.get().strip().lower()
        finally:
            entry.destroy()
            button.destroy()

    def _dialog(self, title, message, choices):
        """Wait for a choice; the X button uses the last (dismiss/no) choice."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.transient(self.root)
        answer = choices[-1][1]

        def choose(value):
            nonlocal answer
            answer = value
            self.root.quit()

        window.protocol('WM_DELETE_WINDOW', lambda: choose(choices[-1][1]))
        tk.Label(window, text=message).pack(padx=20, pady=20)
        for label, value in choices:
            tk.Button(window, text=label, command=lambda value=value: choose(value)).pack(pady=10)
        window.grab_set()
        try:
            self._wait()
            return answer
        finally:
            window.grab_release()
            window.destroy()

    def display_invalid_guess(self):
        self._dialog('Error:Invalid Guess', 'Invalid word size. Enter word of correct size', [('Close', None)])

    def display_win(self):
        self._dialog('You won!', 'Congrats, You guessed the word!', [('Woohoo!', None)])

    def display_loss(self):
        self._dialog('You Lost!', 'Out of Attempts, Game Over!', [('Darn!', None)])

    def display_play_again(self):
        return self._dialog('Continue?', 'Would you like to play again?', [('Yes', True), ('No', False)])

    def say_goodbye(self):
        self._dialog('Closing App...', 'Goodbye!', [('Bye', None)])

    def display_word_to_guess(self, word_to_guess):
        self._dialog('The answer was...', f'The word was {word_to_guess}!', [('ok', None)])
