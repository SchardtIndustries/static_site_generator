from markdown_to_html import markdown_to_html_node
from htmlnode import HTMLNode

def test_markdown_to_html_node():
    # Test 1: Basic header
    md1 = "# Heading 1"
    node1 = markdown_to_html_node(md1)
    assert isinstance(node1, HTMLNode)
    assert any(child.tag == 'h1' for child in node1.children), "h1 header missing"
    h1_node = next(child for child in node1.children if child.tag == 'h1')
    assert any(c.value == 'Heading 1' for c in h1_node.children), "Heading text missing"

    # Test 2: List items
    md2 = "- List item 1\n- List item 2"
    node2 = markdown_to_html_node(md2)
    # The top-level should contain a <ul> with <li> children
    ul_node = None
    for child in node2.children:
        if child.tag == 'ul':
            ul_node = child
            break
    assert ul_node is not None, "Unordered list missing"
    assert all(li.tag == 'li' for li in ul_node.children), "List items missing"
    list_texts = [li.children[0].value for li in ul_node.children]
    assert "List item 1" in list_texts
    assert "List item 2" in list_texts

    # Test 3: Second-level header with bold and italic
    md3 = "## Heading 2\n\nSome **bold** and *italic* text."
    node3 = markdown_to_html_node(md3)
    # Check for h2 header
    h2 = None
    for child in node3.children:
        if child.tag == 'h2':
            h2 = child
            break
    assert h2 is not None and any(c.value == 'Heading 2' for c in h2.children), "h2 header missing"
    # Check for paragraph with bold and italic
    paragraph = None
    for child in node3.children:
        if child.tag == 'p':
            paragraph = child
            break
    assert paragraph is not None
    # Check that paragraph contains text nodes with bold and italic
    bold_node = None
    italic_node = None
    for c in paragraph.children:
        if c.tag == 'strong':
            bold_node = c
        elif c.tag == 'em':
            italic_node = c
    assert bold_node is not None and any(c.value == 'bold' for c in bold_node.children), "Bold text missing"
    assert italic_node is not None and any(c.value == 'italic' for c in italic_node.children), "Italic text missing"

    print("All tests passed!")

# Run the tests
test_markdown_to_html_node()
