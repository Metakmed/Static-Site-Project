import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInline(unittest.TestCase):
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

    def test_text_to_textnode(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_text_to_textnode_plain(self):
        new_nodes = text_to_textnodes(
            "This is just normal text no markdown syntax here"
        )
        self.assertListEqual(
            [
                TextNode("This is just normal text no markdown syntax here", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnode_singular_type(self):
        new_nodes = text_to_textnodes(
            "**Oops all bold text here, sorry!**"
        )
        self.assertListEqual(
            [
                TextNode("Oops all bold text here, sorry!", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_text_to_textnode_multiple_bold(self):
        new_nodes = text_to_textnodes(
            "**Oops all bold text here, sorry!****Honestly it's all just bold text****IM SERIOUSLY BOLD!**"
        )
        self.assertListEqual(
            [
                TextNode("Oops all bold text here, sorry!", TextType.BOLD),
                TextNode("Honestly it's all just bold text", TextType.BOLD),
                TextNode("IM SERIOUSLY BOLD!", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_text_to_textnode_multiple_image(self):
        new_nodes = text_to_textnodes(
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![luke image](https://i.imgur.com/HLK8w9j.jpeg)![leia image](https://i.imgur.com/tUhp6g2.jpeg)"
        )
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("luke image", TextType.IMAGE, "https://i.imgur.com/HLK8w9j.jpeg"),
                TextNode("leia image", TextType.IMAGE, "https://i.imgur.com/tUhp6g2.jpeg")
            ],
            new_nodes,
        )
    def test_text_to_textnode_bold_start(self):
        new_nodes = text_to_textnodes(
            "**Oops all bold text here, sorry!** I lied this is not bold text."
        )
        self.assertListEqual(
            [
                TextNode("Oops all bold text here, sorry!", TextType.BOLD),
                TextNode(" I lied this is not bold text.", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnode_image_start(self):
        new_nodes = text_to_textnodes(
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) Oh look an image of obi wan!"
        )
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" Oh look an image of obi wan!", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnode_link_start(self):
        new_nodes = text_to_textnodes(
            "[obi wan fanpage](https://i.imgur.com) Oh look an link to a obi wan fanpage!"
        )
        self.assertListEqual(
            [
                TextNode("obi wan fanpage", TextType.LINK, "https://i.imgur.com"),
                TextNode(" Oh look an link to a obi wan fanpage!", TextType.TEXT),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
