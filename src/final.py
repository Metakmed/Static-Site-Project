from block import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from inline import text_to_children
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown_doc: str)-> ParentNode:
    blocks = markdown_to_blocks(markdown_doc)
    head_children = []
    head_node = ParentNode("div", head_children)

    for block in blocks:
        block_children = []
        split_block = block.split("\n")
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            formated_text = block[3:len(block)-3].lstrip("\n")
            block_node = ParentNode(block_type.value, [text_node_to_html_node(TextNode(formated_text, TextType.TEXT))] )
            special_case = ParentNode("pre", [block_node])
            head_children.append(special_case)

        elif block_type == BlockType.HEADING:
            count = 0
            split_text = block.split(" ", 1)
            formated_text = split_text[1].strip()
            for i in split_text[0]:
                if i == "#":
                    count += 1
            block_children.extend(text_to_children(formated_text))
            block_node = ParentNode(f"h{count}", block_children)
            head_children.append(block_node)

        elif block_type == BlockType.QUOTE:
            formated_list = []
            for line in split_block:
                if line:
                    formated_list.append(line.lstrip(">").strip())
            block_children.extend(text_to_children(" ".join(formated_list)))
            block_node = ParentNode(block_type.value, block_children)
            head_children.append(block_node)

        elif block_type == BlockType.UNORDERED_LIST:
            for line in split_block:
                if line:
                    block_children.append(ParentNode("li", text_to_children(line[2:])))
            block_node = ParentNode(block_type.value, block_children)
            head_children.append(block_node)

        elif block_type == BlockType.ORDERED_LIST:
            for line in split_block:
                if line:
                    split_line = line.split(". ", 1)
                    block_children.append(ParentNode("li", text_to_children(split_line[1])))
            block_node = ParentNode(block_type.value, block_children)
            head_children.append(block_node)

        elif block_type == BlockType.PARAGRAPH:
            formated_list = []
            for line in split_block:
                if line:
                    formated_list.append(line.strip())
            block_children.extend(text_to_children(" ".join(formated_list)))
            block_node = ParentNode(block_type.value, block_children)
            head_children.append(block_node)


    return head_node
