import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType, Enum


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag='div', value='Content', props={})
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_single_attribute(self):
        node = HTMLNode(tag='a', value='Link', props={'href': 'https://www.google.com'})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_attributes(self):
        props = {
            'href': 'https://www.google.com',
            'target': '_blank',
            'rel': 'noopener'
        }
        node = HTMLNode(tag='a', value='Link', props=props)
        expected = ' href="https://www.google.com" target="_blank" rel="noopener"'
        self.assertEqual(node.props_to_html(), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")
        
    def test_leaf_with_none_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
        
    def test_leaf_with_empty_string_value(self):
        node = LeafNode("div", "")
        self.assertEqual(node.to_html(), "<div></div>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag_raises(self):
        with self.assertRaises(ValueError):
            parent = ParentNode(None, [LeafNode("p", "Text")])
            parent.to_html()

    def test_to_html_without_children_raises(self):
        with self.assertRaises(ValueError):
            parent = ParentNode("div", None)
            parent.to_html()

    def test_to_html_with_no_children_but_with_tag(self):
        # Should produce an empty container with no children
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_nested_multiple_children(self):
        grandchild1 = LeafNode("b", "bold")
        grandchild2 = LeafNode("i", "italic")
        child1 = LeafNode("p", "Para")
        child2 = ParentNode("span", [grandchild1, grandchild2])
        parent = ParentNode("section", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<section><p>Para</p><span><b>bold</b><i>italic</i></span></section>",
        )

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_raw_text(self):
        tnode = TextNode("Sample text", TextType.PLAIN)
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertIsNone(leaf.tag)
        self.assertEqual(leaf.value, "Sample text")
    
    def test_bold_text(self):
        tnode = TextNode("Bold text", TextType.BOLD)
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.value, "Bold text")
    
    def test_italic_text(self):
        tnode = TextNode("Italic text", TextType.ITALIC)
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.tag, "i")
        self.assertEqual(leaf.value, "Italic text")
    
    def test_code_text(self):
        tnode = TextNode("print()", TextType.CODE)
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.tag, "code")
        self.assertEqual(leaf.value, "print()")
    
    def test_link_with_url(self):
        tnode = TextNode("Google", TextType.LINK, url="https://www.google.com")
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.value, "Google")
        self.assertIn("href", leaf.props)
        self.assertEqual(leaf.props["href"], "https://www.google.com")
    
    def test_link_without_url_raises(self):
        tnode = TextNode("Broken link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(tnode)
    
    def test_image_with_src_and_alt(self):
        tnode = TextNode("alt text", TextType.IMAGE, url="https://image.url/image.png")
        leaf = text_node_to_html_node(tnode)
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.value, "")
        self.assertIn("src", leaf.props)
        self.assertEqual(leaf.props["src"], "https://image.url/image.png")
        self.assertIn("alt", leaf.props)
        self.assertEqual(leaf.props["alt"], "alt text")
    
    def test_image_without_src_raises(self):
        tnode = TextNode("alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(tnode)
    
    def test_unknown_type_raises(self):
        class FakeType(Enum):
            UNKNOWN = "unknown"
        tnode = TextNode("dummy", FakeType.UNKNOWN)
        with self.assertRaises(ValueError):
            text_node_to_html_node(tnode)

if __name__ == "__main__":
    unittest.main()
