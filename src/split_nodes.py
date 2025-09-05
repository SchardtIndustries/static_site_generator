import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        index = 0
        start_idx = 0
        length = len(text)

        while index < length:
            if text.startswith(delimiter, index):
                if start_idx != index:
                    new_nodes.append(TextNode(text[start_idx:index], TextType.PLAIN))
                index += len(delimiter)
                end_index = text.find(delimiter, index)
                if end_index == -1:
                    remaining_text = text[start_idx:]
                    new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
                    return new_nodes
                segment_text = text[index:end_index]
                new_nodes.append(TextNode(segment_text, text_type))
                index = end_index + len(delimiter)
                start_idx = index
            else:
                index += 1

        if start_idx < length:
            remaining_text = text[start_idx:]
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r'!\[([^\]]*)\]\((https?://[^\)]*)?\)'
    for node in old_nodes:
        if node.text_type != "TEXT":
            new_nodes.append(node)
            continue
        last_index = 0
        for match in re.finditer(pattern, node.text):
            start, end = match.span()
            alt_text = match.group(1)
            url = match.group(2) if match.group(2) else ''
            # preceding text
            if start > last_index:
                new_nodes.append(TextNode(node.text[last_index:start], "TEXT"))
            # image node
            new_nodes.append(TextNode(alt_text, "IMAGE", url))
            last_index = end
        # remaining text after last match
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], "TEXT"))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r'\[([^\]]*)\]\((https?://[^\)]*)?\)'
    for node in old_nodes:
        # Only process text nodes for links
        if node.text_type != "TEXT" or "[" not in node.text:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in re.finditer(pattern, node.text):
            start, end = match.span()
            link_text = match.group(1)
            url = match.group(2) if match.group(2) else ''
            # preceding text
            if start > last_index:
                new_nodes.append(TextNode(node.text[last_index:start], "TEXT"))
            # link node
            new_nodes.append(TextNode(link_text, "LINK", url))
            last_index = end
        # remaining text
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], "TEXT"))
    return new_nodes

# Adjusted code with TextType set to "PLAIN" for the initial node

def text_to_textnodes(text):
    # Start with one node with text with type "PLAIN"
    nodes = [TextNode(text, "PLAIN")]

    def split_bold(nodes):
        pattern = r'\*\*([^\*]+)\*\*'
        result = []
        for node in nodes:
            if node.text_type != "PLAIN":
                result.append(node)
                continue
            last_idx = 0
            for match in re.finditer(pattern, node.text):
                start, end = match.span()
                if start > last_idx:
                    result.append(TextNode(node.text[last_idx:start], "PLAIN"))
                result.append(TextNode(match.group(1), "BOLD"))
                last_idx = end
            if last_idx < len(node.text):
                result.append(TextNode(node.text[last_idx:], "PLAIN"))
        return result

    def split_italic(nodes):
        pattern = r'_(.+?)_'
        result = []
        for node in nodes:
            if node.text_type != "PLAIN":
                result.append(node)
                continue
            last_idx = 0
            for match in re.finditer(pattern, node.text):
                start, end = match.span()
                if start > last_idx:
                    result.append(TextNode(node.text[last_idx:start], "PLAIN"))
                result.append(TextNode(match.group(1), "ITALIC"))
                last_idx = end
            if last_idx < len(node.text):
                result.append(TextNode(node.text[last_idx:], "PLAIN"))
        return result

    def split_code(nodes):
        pattern = r'`([^`]+)`'
        result = []
        for node in nodes:
            if node.text_type != "PLAIN":
                result.append(node)
                continue
            last_idx = 0
            for match in re.finditer(pattern, node.text):
                start, end = match.span()
                if start > last_idx:
                    result.append(TextNode(node.text[last_idx:start], "PLAIN"))
                result.append(TextNode(match.group(1), "CODE"))
                last_idx = end
            if last_idx < len(node.text):
                result.append(TextNode(node.text[last_idx:], "PLAIN"))
        return result

    def split_images(nodes):
        pattern = r'!\[([^\]]*)\]\((https?://[^\)]*)?\)'
        result = []
        for node in nodes:
            if node.text_type != "PLAIN":
                result.append(node)
                continue
            last_idx = 0
            for match in re.finditer(pattern, node.text):
                start, end = match.span()
                alt_text = match.group(1)
                url = match.group(2) if match.group(2) else ''
                if start > last_idx:
                    result.append(TextNode(node.text[last_idx:start], "PLAIN"))
                result.append(TextNode(alt_text, "IMAGE", url))
                last_idx = end
            if last_idx < len(node.text):
                result.append(TextNode(node.text[last_idx:], "PLAIN"))
        return result

    def split_links(nodes):
        pattern = r'\[([^\]]*)\]\((https?://[^\)]*)?\)'
        result = []
        for node in nodes:
            if node.text_type != "PLAIN" or "[" not in node.text:
                result.append(node)
                continue
            last_idx = 0
            for match in re.finditer(pattern, node.text):
                start, end = match.span()
                link_text = match.group(1)
                url = match.group(2) if match.group(2) else ''
                if start > last_idx:
                    result.append(TextNode(node.text[last_idx:start], "PLAIN"))
                result.append(TextNode(link_text, "LINK", url))
                last_idx = end
            if last_idx < len(node.text):
                result.append(TextNode(node.text[last_idx:], "PLAIN"))
        return result

    # Sequentially apply the splitting functions
    nodes = split_bold(nodes)
    nodes = split_italic(nodes)
    nodes = split_code(nodes)
    nodes = split_images(nodes)
    nodes = split_links(nodes)

    return nodes
