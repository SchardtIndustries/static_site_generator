import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

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
        # Remaining text includes the open delimiter
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
        # Verify all code segments are correctly identified
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
        # Nodes that are not plain should be passed through unchanged
        node = TextNode("already formatted", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn(node, result)

if __name__ == '__main__':
    unittest.main()
