from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception(f"Invalid text_node type: {text_node.text_type}")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, prop={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", prop={"src": text_node.url, "alt": text_node.text})


if __name__ == "__main__":
    text_node = TextNode("This is a text node", "bold")

    parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(text_node)
