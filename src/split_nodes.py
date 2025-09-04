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
                # Python
                if end_index == -1:
                    # No closing delimiter found: include everything from start_idx
                    remaining_text = text[start_idx:]
                    new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
                    return new_nodes
                # Append enclosed text
                segment_text = text[index:end_index]
                new_nodes.append(TextNode(segment_text, text_type))
                index = end_index + len(delimiter)
                start_idx = index
            else:
                index += 1

        # Append any remaining text *after* the last delimiter or unclosed delimiter
        if start_idx < length:
            remaining_text = text[start_idx:]
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes
