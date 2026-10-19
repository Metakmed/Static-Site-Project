from textnode import TextNode, TextType

def main():
    test_node = TextNode("This is normal text", TextType.BASIC, TextType.LINK)
    print(test_node)
main()
