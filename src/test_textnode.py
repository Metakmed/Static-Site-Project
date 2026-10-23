import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node",TextType.BOLD)
        node2 = TextNode("This is a text node",TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node",TextType.BOLD, TextType.LINK)
        node4 = TextNode("This is a text node",TextType.BOLD, TextType.LINK)
        self.assertEqual(node3, node4)

        node3 = TextNode("This is a text node",TextType.BOLD)
        node4 = TextNode("This is a text node",TextType.BOLD, None)
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        node = TextNode("This is a text node",TextType.BOLD)
        node2 = TextNode("This is a text node",TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node",TextType.BOLD, TextType.LINK)
        node4 = TextNode("This is a text node",TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        text_html_node = text_node_to_html_node(text_node)
        self.assertEqual(text_html_node.tag, None)
        self.assertEqual(text_html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic_text(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code_text(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link_text(self):
        node = TextNode("This is a link text node", TextType.LINK, "http://CoolGuyz.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "http://CoolGuyz.com"})

    def test_image_text(self):
        node = TextNode("This is a image text node", TextType.IMAGE, "http://CoolGuyz.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://CoolGuyz.com", "alt": "This is a image text node"})

    def test_split_nodes_delimiter_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_bold(self):
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes2, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    def test_split_nodes_delimiter_italic(self):
        node3 = TextNode("This is text with a __italic__ word", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], "__", TextType.ITALIC)
        self.assertEqual(new_nodes3, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This is text with a **bold** word and another **bold** word and another **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ])
    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This word is **bold", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter,[node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
