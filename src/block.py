def markdown_to_blocks(markdown_text:str):
    new_blocks = []
    result = []
    split_blocks = markdown_text.split("\n\n")
    for block in split_blocks:
        stripped_block = block.strip()
        new_blocks.append(stripped_block)
    for block in new_blocks:
        if block:
            result.append(block)
    return result
