import unittest

from main import extract_title


class TestGenerate(unittest.TestCase):
    def test_extract_title(self):
        md = """# This is a title!

This is a paragraph
realating to the
title!
"""
        title = extract_title(md)
        self.assertEqual("This is a title!", title)

    def test_extract_title_invalid(self):
        md = """This an inncorect title!

This is a paragraph
realating to the
incorrect title!
"""
        self.assertRaises(ValueError, extract_title, md)

if __name__ == "__main__":
    unittest.main()
