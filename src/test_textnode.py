import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq_different_text(self):
        node1 = TextNode("Text one", TextType.PLAIN)
        node2 = TextNode("Text two", TextType.PLAIN)
        self.assertNotEqual(node1, node2)
        
    def test_neq_different_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
        
    def test_neq_different_url(self):
        node1 = TextNode("Link", TextType.LINK, url="http://example.com")
        node2 = TextNode("Link", TextType.LINK, url="http://another.com")
        self.assertNotEqual(node1, node2)
        
    def test_repr_format(self):
        node = TextNode("Sample", TextType.ITALIC, url="http://test.com")
        expected_repr = "TextNode(Sample, italic, http://test.com)"
        self.assertEqual(repr(node), expected_repr)
        
    def test_compare_with_different_object_type(self):
        node = TextNode("Sample", TextType.PLAIN)
        self.assertNotEqual(node, "a string")
        
    def test_node_with_none_url_and_different_property(self):
        node1 = TextNode("Sample", TextType.PLAIN)
        node2 = TextNode("Sample", TextType.BOLD)
        self.assertNotEqual(node1, node2)
        
    def test_node_with_same_properties_both_none_url(self):
        node1 = TextNode("Sample", TextType.ITALIC)
        node2 = TextNode("Sample", TextType.ITALIC)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
