import unittest
from unittest.mock import Mock

from controller.game_controller import GameController
from model.game import game
from view.game_view_GUI import GameClosed, GameViewGUI


class ControllerTests(unittest.TestCase):
    def test_invalid_guess_win_replay_loss_and_exit(self):
        model = game()
        model.get_all_words_of_size = lambda: ['apple']
        view = Mock()
        view.get_guess.side_effect = ['bad', 'apple'] + ['zzzzz'] * 6
        view.display_play_again.side_effect = [True, False]

        GameController(model, view).run_game()

        view.display_invalid_guess.assert_called_once()
        view.display_win.assert_called_once()
        view.display_loss.assert_called_once()
        self.assertEqual(view.display_word_to_guess.call_count, 2)
        view.say_goodbye.assert_called_once()
        self.assertEqual(model.player.lives_left, model.player.lives_start)
        self.assertTrue(all(cell == [' ', ' '] for row in model.board.board for cell in row))

    def test_closing_window_unwinds_wait(self):
        view = object.__new__(GameViewGUI)
        view.root = Mock()
        view.closed = False
        view.root.mainloop.side_effect = view.close

        with self.assertRaises(GameClosed):
            view._wait()
        view.root.quit.assert_called_once()
