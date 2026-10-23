class HTMLNode:
    def __init__(self, tag:str | None =None, value:str | None =None, children:list[HTMLNode] | None =None, props:dict[str, str] | None =None) -> None:
        self.tag = tag # <p>, <a>, <h1>, etc
        self.value = value # The text
        self.children = children # list of HTMLNode objects
        self.props = props # Dict of kvp representing the attributes of the HTML tag

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
    def __init__(self, tag:str | None, value:str, props:dict[str, str] | None=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self)-> str:
        if self.value is None or not self.value:
            raise ValueError("Invalid HTML: no value")

        if self.tag is None:
            return self.value

        link = self.props_to_html()
        return f"<{self.tag}{link}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid Tag: no value")

        if not self.children:
            raise ValueError("Invalid Children: no value")
        children = ""
        for child in self.children:
            to_add = child.to_html()
            children += to_add
        result = f"<{self.tag}>{children}</{self.tag}>"
        return result
