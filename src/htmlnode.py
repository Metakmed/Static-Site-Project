

class HTMLNode():
    def __init__(self, TAG:str | None =None, VALUE:str | None =None, CHILDREN:list[HTMLNode] | None =None, PROPS:dict[str, str] | None =None) -> None:
        self.tag = TAG # <p>, <a>, <h1>, etc
        self.value = VALUE # The text
        self.children = CHILDREN # list of HTMLNode objects
        self.props = PROPS # Dict of kvp representing the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self)-> str:
        result =""
        if self.props is None:
            return result
        for key in self.props:
           result += "".join(f' {key}="{self.props[key]}"')
        return result

    def __eq__(self, other) -> bool:
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, TAG:str, VALUE:str, PROPS:dict[str, str] | None=None) -> None:
        super().__init__(TAG, VALUE, None, PROPS)

    def to_html(self)-> str:
        if self.value is None or not self.value:
            raise ValueError("Invalid HTML: no value")

        if self.tag is None:
            return self.value

        link = self.props_to_html()
        return f"<{self.tag}{link}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
