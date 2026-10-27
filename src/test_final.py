import unittest

from final import markdown_to_html_node


class TestFinal(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """# This is a heading!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading!</h1></div>",
        )

    def test_headingblock_multiple(self):
        md = """###### This is a heading!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading!</h6></div>",
        )

    def test_unorderedblock(self):
        md = """- Item 1
- Item 2
- Item 3
- Item 4
- Item 5
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li></ul></div>",
        )
    def test_orderedblock(self):
        md = """1. Item 1
2. Item 2
3. Item 3
4. Item 4
5. Item 5
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li></ol></div>",
        )

    def test_orderedblock_outordered(self):
        md = """6. Item 1
2. Item 2
4. Item 3
3. Item 4
5. Item 5
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>6. Item 1 2. Item 2 4. Item 3 3. Item 4 5. Item 5</p></div>",
        )

    def test_quoteblock(self):
        md = """>This is a quote!
> This is also a quote!
>This is my final quote!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote! This is also a quote! This is my final quote!</blockquote></div>",
        )

    def test_multipleblocks(self):
        md = """This should be text
within a p tag

# This is a heading block!

1. Numba 1
2. Numba 2
3. Numba 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This should be text within a p tag</p><h1>This is a heading block!</h1><ol><li>Numba 1</li><li>Numba 2</li><li>Numba 3</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
