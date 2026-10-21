from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "some text"
    BOLD = "**bold text**"
    ITALIC = "_italic text_"
    CODE =  "`code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url:str | None =None) -> None:
        self.txt = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.url == other.url and self.txt == other.txt and self.text_type == other.text_type

    def __repr__(self) -> str:
        if self.url is None:
            return f"TextNode({self.txt}, {self.text_type.value}, None)"
        return f"TextNode({self.txt}, {self.text_type.value}, {self.url.value})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type in TextType:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.txt)

        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.txt)

        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.txt)

        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.txt)

        if text_node.text_type == TextType.LINK:
            if text_node.url:
                return LeafNode("a", text_node.txt, {"href": text_node.url})
            raise Exception("TextType is LINK but url is None")

        if text_node.text_type == TextType.IMAGE:
            if text_node.url:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.txt})
            raise Exception("TextType is IMAGE but url is None")

    raise Exception("Invalid Text Type: no or incorrect value")
