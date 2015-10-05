# -*- coding: utf-8 -*-
import os
import unittest

import scrubber

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
_DIR = os.path.join(BASE_DIR, "test_data")

cleaned_text = "\nLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\n"

original_text = None
with open(os.path.join(_DIR, 'infected_1.txt'), 'r') as fp:
    original_text = fp.read()

class TestScrubber(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        with open(os.path.join(_DIR, 'infected_1.txt'), 'w') as fp:
            fp.seek(0, 0)
            fp.write(original_text)

    def test_find_infections(self):
        find = scrubber.find_infected(_DIR)

        self.assertEqual(len(find), 1)
        self.assertEqual(find[0], os.path.join(_DIR, "infected_1.txt"))

    def test_remove_infections(self):
        rm = scrubber.remove_infected(_DIR)

        self.assertEqual(len(rm), 1)
        with open(os.path.join(_DIR, 'infected_1.txt'), 'rw') as fp:
            self.assertEqual(fp.read(), cleaned_text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
