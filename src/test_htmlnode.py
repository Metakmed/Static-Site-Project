import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("<a>", "Some Text", PROPS=props)
        node2 = HTMLNode("<a>", "Some Text", PROPS=props)

        nodes:list[HTMLNode] = [node, node2]

        node3 = HTMLNode("<a>", CHILDREN=nodes)
        node4 = HTMLNode("<a>", CHILDREN=nodes)
        node5 = HTMLNode("<a>", "Some Text")
        node6 = HTMLNode("<a>", "Some Text")

        self.assertEqual(node3, node4)

        self.assertEqual(node, node2)

        self.assertEqual(node5, node6)



    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("<a>", "Some Text", PROPS=props)
        node2 = HTMLNode("<a>", "Some Text", PROPS=props)

        html = node.props_to_html()
        html2 = node2.props_to_html()

        self.assertEqual(html, html2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
