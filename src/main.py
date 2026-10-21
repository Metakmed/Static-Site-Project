from textnode import TextNode, TextType

def main():
    test_node = TextNode("This is normal text", TextType.TEXT, TextType.LINK)
    print(test_node)
main()
