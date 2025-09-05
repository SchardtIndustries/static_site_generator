import re

def markdown_to_blocks(markdown):
    # Split on blank lines (lines that are empty or contain only whitespace)
    # The pattern matches two or more newlines possibly with whitespace in between
    blocks = re.split(r'\n\s*\n', markdown.strip())
    # Strip whitespace from each block and filter out empty ones
    return [block.strip() for block in blocks if block.strip()]
