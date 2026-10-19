import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
