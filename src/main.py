from textnode import TextNode
from htmlnode import ParentNode, LeafNode

text_node = TextNode("This is a text node",
                     "bold",
                     "https://www.boot.dev")

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
print(parent_node)
