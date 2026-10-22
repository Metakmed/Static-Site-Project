import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("This is just plain text with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links("This is just plain text with no links.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        text = "![image](https://example.com/img.png) and [a link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("a link", "https://example.com")], matches)

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode(
            "This is text with two ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com) and another [second link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode(
            "This is text with two [link](https://i.imgur.com)[second link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode("second link", TextType.LINK, "https://i.imgur.com"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
