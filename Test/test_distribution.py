import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from model.game import game


class DistributionTests(unittest.TestCase):
    def test_word_list_from_another_working_directory(self):
        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                words = game().get_all_words_of_size()
            finally:
                os.chdir(original_directory)
        self.assertTrue(words)
        self.assertTrue(all(len(word) == 5 for word in words))

    def test_single_word_can_be_selected(self):
        model = game()
        self.assertEqual(model.pick_word_to_guess(['apple']), 'apple')
        self.assertEqual(model.word_to_guess, 'apple')

    def test_random_selection_stays_in_word_list(self):
        model = game()
        words = model.get_all_words_of_size()
        for _ in range(1000):
            self.assertIn(model.pick_word_to_guess(words), words)

    def test_console_completes_game_outside_repo(self):
        entrypoint = Path(__file__).resolve().parent.parent / 'mainConsole.py'
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(entrypoint)], cwd=directory,
                input='zzzzz\n' * 6 + 'n\n', text=True,
                capture_output=True, timeout=15,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Out of attempts. Game over!', result.stdout)
        self.assertIn('Goodbye!', result.stdout)
