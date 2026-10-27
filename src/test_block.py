import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_block_to_block_type_paragraph(self):
        block = """
This is normal text
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiple_lines(self):
        block = """
This is normal text
This is more Normal Text
More text
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_quote(self):
        block = """This is normal text
>This is more Normal Text
More text
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = """# This is a heading"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_no_space(self):
        block = """#This is not a heading
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_no_text(self):
        block = "# "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block ="""```
This is code
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_multiple(self):
        block ="""```
This is code
THis is more code

CODE
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_incorrect(self):
        block ="""``
This is code
THis is more code

CODE
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered(self):
        block ="""- Text 1"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_multiple(self):
        block ="""- Text 1
- Text 3
- Text 2"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_invalid_line(self):
        block ="""- Text 1
    > Quote
    - Text 2"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered(self):
        block ="""1. numba 1
2. numba 2
3. numba 3"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_unordered(self):
        block ="""1. numba 1
3. numba 2
2. numba 3"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_missing_whitespace(self):
        block ="""1.nospace
2.nospace"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
