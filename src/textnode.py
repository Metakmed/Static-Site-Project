from enum import Enum

class TextType(Enum):
    TEXT = "some text"
    BOLD = "**bold text**"
    ITALIC = "_italic text_"
    CODE =  "`code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None) -> None:
        self.txt = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other) -> bool:
        return self.url == other.url and self.txt == other.txt and self.text_type == other.text_type

    def __repr__(self) -> str:
        return f"TextNode({self.txt}, {self.text_type.value}, {self.url.value})"
