from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        if not self.props:
            return ''
        attrs = ''
        for key, val in self.props.items():
            attrs += f' {key}="{val}"'
        return attrs

    def __repr__(self):
        return (f"HTMLNode("
                f"tag={self.tag!r}, "
                f"value={getattr(self, 'value', None)!r}, "
                f"children={self.children!r}, "
                f"props={self.props!r})")

    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("A leaf node must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        attrs = self.props_to_html()
        voids = {'img', 'br', 'hr', 'meta', 'link', 'input'}
        if self.tag in voids:
            return f"<{self.tag}{attrs}>"
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag.")
        if children is None:
            raise ValueError("ParentNode must have children.")
        self.tag = tag
        self.children = children
        self.props = props if props is not None else []

    def to_html(self):
        if self.tag is None:
            raise ValueError("Cannot render HTML without a tag.")
        if self.children is None:
            raise ValueError("Parent node must have children.")
        attrs = self.props_to_html()
        inner_html = ''
        for child in self.children:
            # Each child is expected to have a to_html method
            inner_html += child.to_html()
        return f"<{self.tag}{attrs}>{inner_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Input must be a TextNode.")

    if text_node.text_type == TextType.PLAIN:
        # Raw text without any tag
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        # Bold text wrapped in <b>
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        # Italic text wrapped in <i>
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        # Code text wrapped in <code>
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        # Link with href prop
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL.")
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        # Image with src and alt props
        if not text_node.url:
            raise ValueError("Image TextNode must have a src (URL).")
        alt_text = text_node.text if text_node.text else ''
        return LeafNode("img", "", props={"src": text_node.url, "alt": alt_text})
    else:
        # If an unknown TextType, raise an exception
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
