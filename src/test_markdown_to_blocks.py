from markdown_to_blocks import markdown_to_blocks

def test_markdown_to_blocks():
    markdown = (
        "# This is a heading\n\n"
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        "- This is the first list item in a list block\n"
        "- This is a list item\n"
        "- This is another list item"
    )

    # python
    expected_blocks = [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
    ]

    result_blocks = markdown_to_blocks(markdown)

    assert result_blocks == expected_blocks, f"Expected {expected_blocks}, but got {result_blocks}"
    print("test_markdown_to_blocks passed!")

# Run the test
test_markdown_to_blocks()
