import re

from textnode import TextNode, TextType, split_nodes_delimiter


def extract_markdown_images(markdown_text: str):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown_text)
    return result

def extract_markdown_links(markdown_text: str):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown_text)
    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        current_txt = node.txt
        if node.text_type is TextType.TEXT:
            images = extract_markdown_images(node.txt)
            if not images:
                new_nodes.append(node)
            else:
                for image in images:
                    split_txt = current_txt.split(f"![{image[0]}]({image[1]})", 1)
                    if len(split_txt) != 2:
                        raise Exception("Error: invalid markdown syntax")
                    if split_txt[0] != "":
                        new_nodes.append(TextNode(split_txt[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    current_txt = split_txt[1]
                if current_txt != "":
                    new_nodes.append(TextNode(current_txt, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        current_txt = node.txt
        if node.text_type is TextType.TEXT:
            links = extract_markdown_links(node.txt)
            if not links:
                new_nodes.append(node)
            else:
                for link in links:
                    split_txt = current_txt.split(f"[{link[0]}]({link[1]})", 1)
                    if len(split_txt) != 2:
                        raise Exception("Error: invalid markdown syntax")
                    if split_txt[0] != "":
                        new_nodes.append(TextNode(split_txt[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    current_txt = split_txt[1]
                if current_txt != "":
                    new_nodes.append(TextNode(current_txt, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(markdown_text:str):
    starting_node = TextNode(markdown_text, TextType.TEXT)
    starting_list = [starting_node]
    new_nodes = split_nodes_delimiter(starting_list, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    return new_nodes
