import unittest

from block import markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ]
            )

    def test_markdown_to_blocks_blanks(self):
        md = """
        # Block 1




        # Block 2
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Block 1", "# Block 2"])

    def test_markdown_to_blocks_leading_and_trailing_whitespaces(self):
        md = """


        # Block 1

        # Block 2


        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Block 1", "# Block 2"])

    def test_markdown_to_blocks_whitespace_only_blocks(self):
        md = "# Block 1\n   \n\n# Block 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Block 1", "# Block 2"])

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_document(self):
        md = "   \n\n  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph without any line breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph without any line breaks."])

    def test_markdown_to_blocks_internal_single_line(self):
        md = """
Line 1 of block
Line 2 of block

Second block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1 of block\nLine 2 of block", "Second block"])

if __name__ == "__main__":
    unittest.main()
