import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        properties = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("<a>", "Some Text", props=properties)
        node2 = HTMLNode("<a>", "Some Text", props=properties)

        nodes:list[HTMLNode] = [node, node2]

        node3 = HTMLNode("<a>", children=nodes)
        node4 = HTMLNode("<a>", children=nodes)
        node5 = HTMLNode("<a>", "Some Text")
        node6 = HTMLNode("<a>", "Some Text")

        self.assertEqual(node3, node4)

        self.assertEqual(node, node2)

        self.assertEqual(node5, node6)



    def test_props_to_html(self):
        properties = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("<a>", "Some Text", props=properties)
        node2 = HTMLNode("<a>", "Some Text", props=properties)

        html = node.props_to_html()
        html2 = node2.props_to_html()

        self.assertEqual(html, html2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        child_node1 = LeafNode("p", "child1")
        child_node2 = LeafNode("p", "child2")
        child_node3 = LeafNode("p", "child3")
        child_node4 = LeafNode("p", "child4")
        child_node5 = LeafNode("p", "child5")
        children = [child_node1, child_node2, child_node3, child_node4, child_node5]
        parent_node2 = ParentNode("div", children)
        self.assertEqual(
            parent_node2.to_html(),
            "<div><p>child1</p><p>child2</p><p>child3</p><p>child4</p><p>child5</p></div>"
        )


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_children(self):
        parent = ParentNode("b",[])
        parent2 =ParentNode("b", None)
        self.assertRaises(ValueError,parent.to_html)
        self.assertRaises(ValueError,parent2.to_html)

        parent3= ParentNode("div", [parent])
        self.assertRaises(ValueError,parent3.to_html)
