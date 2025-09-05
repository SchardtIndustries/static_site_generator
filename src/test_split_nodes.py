import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiters(self):
        node = TextNode("This has no delimiters", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This has no delimiters")
        self.assertEqual(result[0].text_type, TextType.PLAIN)

    def test_single_delimiter_pair(self):
        node = TextNode("This is `code` example", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[2].text, " example")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_multiple_delimiters(self):
        text = "Here is `code`, and here is `more code`."
        node = TextNode(text, TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        # Count code segments
        code_segments = [n for n in result if n.text_type == TextType.CODE]
        self.assertEqual(len(code_segments), 2)
        self.assertIn("code", [n.text for n in code_segments])
        self.assertIn("more code", [n.text for n in code_segments])

    def test_unclosed_delimiter(self):
        node = TextNode("Unclosed `delimiter text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result[-1].text, "Unclosed `delimiter text")
        self.assertEqual(len(result), 2)
        self.assertIn("Unclosed", result[0].text)

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("Start `first` middle", TextType.PLAIN),
            TextNode("No delimiters here", TextType.PLAIN),
            TextNode("`second` and `third`", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        code_texts = [n.text for n in result if n.text_type == TextType.CODE]
        self.assertIn("first", code_texts)
        self.assertIn("second", code_texts)
        self.assertIn("third", code_texts)

    def test_delimiter_in_complete_words(self):
        text = "word`inside`word"
        node = TextNode(text, TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "inside")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_empty_input_list(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_non_plain_node(self):
        node = TextNode("already formatted", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn(node, result)


def test_split_nodes_image():
    node = TextNode(
        "This is text with a ![rick](https://i.imgur.com/rick.png) and more ![]() end.",
        "TEXT"
    )
    result = split_nodes_image([node])
    # Expect 5 nodes: TEXT, IMAGE, TEXT, IMAGE, TEXT
    assert len(result) == 5, f"Expected 5 nodes, got {len(result)}"
    assert result[0].text == "This is text with a "
    assert result[0].text_type == "TEXT"
    assert result[1].text == "rick"
    assert result[1].text_type == "IMAGE"
    assert result[1].url == "https://i.imgur.com/rick.png"
    assert result[2].text == " and more "
    assert result[2].text_type == "TEXT"
    assert result[3].text == ""
    assert result[3].text_type == "IMAGE"
    assert result[3].url == ""
    assert result[4].text == " end."
    assert result[4].text_type == "TEXT"
    print("split_nodes_image test passed!")

def test_split_nodes_link():
    node = TextNode(
        "Click [here](https://here.com) or [there](https://there.com) for info.",
        "TEXT"
    )
    result = split_nodes_link([node])
    # Expect 5 nodes: TEXT, LINK, TEXT, LINK, TEXT
    assert len(result) == 5, f"Expected 5 nodes, got {len(result)}"
    assert result[0].text == "Click "
    assert result[0].text_type == "TEXT"
    assert result[1].text == "here"
    assert result[1].text_type == "LINK"
    assert result[1].url == "https://here.com"
    assert result[2].text == " or "
    assert result[2].text_type == "TEXT"
    assert result[3].text == "there"


def test_text_to_textnodes():
    text = "This is **bold** and _italic_ and `code` and an ![img](https://img.url) and [link](https://link.url)"
    nodes = text_to_textnodes(text)

    # Check sequence and content
    expected_sequence = [
        ("This is ", "PLAIN"),
        ("bold", "BOLD"),
        (" and ", "PLAIN"),
        ("italic", "ITALIC"),
        (" and ", "PLAIN"),
        ("code", "CODE"),
        (" and an ", "PLAIN"),
        ("img", "IMAGE", "https://img.url"),
        (" and ", "PLAIN"),
        ("link", "LINK", "https://link.url"),
    ]

    # To make the test more robust, print actual node texts
    for idx, node in enumerate(nodes):
        print(f"Node {idx}: '{node.text}', type: {node.text_type}, url: {getattr(node, 'url', None)}")
        
    # Then compare
    assert len(nodes) == len(expected_sequence), f"Expected {len(expected_sequence)} nodes, got {len(nodes)}"

    for node, expected in zip(nodes, expected_sequence):
        text_value, text_type = expected[0], expected[1]
        assert node.text == text_value, f"Expected text '{text_value}', got '{node.text}'"
        assert node.text_type == text_type, f"Expected type '{text_type}', got '{node.text_type}'"
        if len(expected) == 3:
            # For IMAGE or LINK nodes
            assert node.url == expected[2], f"Expected URL '{expected[2]}', got '{node.url}'"
        else:
            # For PLAIN, BOLD, ITALIC, CODE
            assert not hasattr(node, 'url') or node.url is None, "Expected no URL for this node"

    print("test_text_to_textnodes passed!")


# Run the test
test_text_to_textnodes()

if __name__ == '__main__':
    unittest.main()
