import re
from enum import Enum


class EmptyValue(Exception):
    """ The value has empty"""

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = 'blockquote'
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"



def markdown_to_blocks(markdown_text: str)-> list[str]:
    new_blocks = []
    result: list[str] = []
    split_blocks = markdown_text.split("\n\n")
    for block in split_blocks:
        stripped_block = block.strip()
        new_blocks.append(stripped_block)
    for block in new_blocks:
        if block:
            result.append(block)
    return result

def block_to_block_type(block:str)-> BlockType:
    if block:
        split_block = block.split("\n")
        total_lines = len(split_block)
        if re.findall(r"^```\n(.*)\n```$", block, re.DOTALL):
            return BlockType.CODE

        if re.findall(r"(^#{1,6} .+)",block):
            return BlockType.HEADING

        quote_matches =  re.findall(r"(^> .+|^>[\S]+)", block, re.MULTILINE)
        if len(quote_matches) == total_lines:
            return BlockType.QUOTE

        unordered_matches = re.findall(r"(^- )", block, re.MULTILINE)
        if len(unordered_matches) == total_lines:
            return BlockType.UNORDERED_LIST
        ordered_count = 0
        for i in range(len(split_block)):
            if re.findall(rf"(^{i + 1}[.] )", split_block[i]):
                ordered_count += 1

        if len(split_block) == ordered_count:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
