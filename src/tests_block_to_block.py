from block_to_block import BlockType, block_to_block_type

def test_block_to_block_type():
    # Heading tests
    assert block_to_block_type("# Heading 1") == BlockType.HEADING
    assert block_to_block_type("###### Heading 6") == BlockType.HEADING
    # Note: Extra spaces should still recognize as heading if leading with '#' followed by space
    assert block_to_block_type("  # Heading with spaces") == BlockType.HEADING

    # Code block tests
    code_block = "```python\nprint('Hello')\n```"
    assert block_to_block_type(code_block) == BlockType.CODE
    # Code block with extra spaces 
    code_block_spaces = "   ```\nSome code\n```"
    assert block_to_block_type(code_block_spaces) == BlockType.CODE

    # Quote block tests
    quote_block = "> This is a quote\n> Still a quote"
    assert block_to_block_type(quote_block) == BlockType.QUOTE
    quote_mixed = "> Line 1\n>Line 2"
    assert block_to_block_type(quote_mixed) == BlockType.QUOTE

    # Unordered list tests
    ul_block = "- Item 1\n- Item 2\n- Item 3"
    assert block_to_block_type(ul_block) == BlockType.UNORDERED_LIST
    # With extra spaces
    ul_spaces = "  - Item 1\n  - Item 2"
    assert block_to_block_type(ul_spaces) == BlockType.UNORDERED_LIST

    # Ordered list tests
    ol_block = "1. First\n2. Second\n3. Third"
    assert block_to_block_type(ol_block) == BlockType.ORDERED_LIST
    # Should handle sequential numbering starting from 1
    ol_mixed_spaces = " 1. One\n 2. Two\n 3. Three"
    assert block_to_block_type(ol_mixed_spaces) == BlockType.ORDERED_LIST
    # Non-sequential number should default to paragraph
    bad_ol = "1. One\n3. Two\n4. Three"
    assert block_to_block_type(bad_ol) == BlockType.PARAGRAPH

    # Paragraph (default)
    paragraph = "This is just some text with no special formatting."
    assert block_to_block_type(paragraph) == BlockType.PARAGRAPH

    # Mixed cases, should default to paragraph
    mixed = "Some text\n> Not a quote if multiline\nBut with > in text is just paragraph"
    assert block_to_block_type(mixed) == BlockType.PARAGRAPH

    print("All tests passed!")

# Run tests
test_block_to_block_type()
