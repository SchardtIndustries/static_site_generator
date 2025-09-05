import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown2 import markdown


def parse_attributes(attr_string):
    attrs = {}
    attr_re = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
    for attr_match in attr_re.finditer(attr_string):
        attr_name, attr_value = attr_match.groups()
        attrs[attr_name] = attr_value
    return attrs

def parse_html_to_nodes(html):
    stack = []
    root = ParentNode('root', [])
    current_node = root

    tag_re = re.compile(r'<(/?)(\w+)(.*?)?>')
    void_elements = {'img', 'input', 'br', 'hr', 'meta', 'link'}
    tag_map = {'em': 'i', 'strong': 'b'}

    pos = 0
    while pos < len(html):
        match = tag_re.search(html, pos)
        if not match:
            break

        tag_start, tag_end = match.span()
        is_closing = match.group(1) == '/'
        tag_name = match.group(2).lower()
        attr_string = match.group(3).strip()
        mapped = tag_map.get(tag_name, tag_name)

        # Handle text between tags
        # Handle text between tags
        if tag_start > pos:
            text_content = html[pos:tag_start]
            if text_content:
                # if we're directly inside a blockquote and this is its first child,
                # trim leading whitespace so it follows the <blockquote> immediately
                if current_node.tag == 'blockquote' and not current_node.children:
                    text_content = text_content.lstrip()
                current_node.children.append(LeafNode(None, text_content))

        # Update position
        pos = tag_end

        if is_closing:
            if stack and stack[-1].tag == mapped:
                node = stack.pop()
                # unwrap <p> inside blockquote
                if getattr(node, "_unwrap_into", None) is not None and mapped == 'p':
                    node._unwrap_into.children.extend(node.children)
        # set current_node after popping
                current_node = stack[-1] if stack else root
        else:
            if mapped in void_elements:
                current_node.children.append(LeafNode(mapped, '', parse_attributes(attr_string)))
            else:
                # unwrap <p> if parent is blockquote
                unwrap_p = (mapped == 'p' and current_node.tag == 'blockquote')
                if unwrap_p:
                    placeholder = ParentNode('p', [])
                    placeholder._unwrap_into = current_node
                    stack.append(placeholder)
                    current_node = placeholder
                else:
                    new_node = ParentNode(mapped, [], parse_attributes(attr_string))
                    current_node.children.append(new_node)
                    current_node = new_node
                    stack.append(new_node)

    # Handle any trailing text
    if pos < len(html):
        trailing_text = html[pos:]
        if trailing_text:
            current_node.children.append(LeafNode(None, trailing_text))

    return root

def markdown_to_html_node(markdown_text):
    # Convert markdown to HTML
    html_content = markdown(markdown_text)

    # Parse HTML content into nodes
    return parse_html_to_nodes(html_content)

# Test your function
markdown_text = """
# Heading 1

- List item 1
- List item 2

## Heading 2

Some **bold** text and some *italic* text.
"""

html_node = markdown_to_html_node(markdown_text)
print(html_node)
