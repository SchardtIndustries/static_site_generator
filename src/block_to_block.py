import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


import re

def block_to_block_type(block):
    lines = block.splitlines()

    # Check for code block start/end (allow leading spaces)
    if lines and lines[0].lstrip().startswith("```") and lines[-1].strip() == "```":
        return BlockType.CODE

    # Check for heading (allow leading spaces)
    first_line_stripped = lines[0].lstrip()
    heading_match = re.match(r'^(#{1,6}) +', first_line_stripped)
    if heading_match:
        return BlockType.HEADING

    # Check for quote
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list
    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list
    ordered_list_match = re.compile(r'^(\d+)\. ')
    expected_number = 1
    for line in lines:
        line_lstripped = line.lstrip()
        match = ordered_list_match.match(line_lstripped)
        if not match:
            break
        number = int(match.group(1))
        if number != expected_number:
            break
        expected_number += 1
    else:
        # All lines matched sequentially
        return BlockType.ORDERED_LIST

    # Default
    return BlockType.PARAGRAPH
