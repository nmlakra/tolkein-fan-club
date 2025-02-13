from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode


def validate_markdown(text, delimiter):

    delimiter_count = 0
    n = len(text)
    m = len(delimiter)
    for i in range(n):
        if text[i: i+m] == delimiter:
            delimiter_count += 1
    if delimiter_count % 2 != 0:
        raise Exception("Invalid markdown syntax found!")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        validate_markdown(node.text, delimiter)

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        buffer = "    "
        texts = (buffer + node.text).split(delimiter)

        for idx, text in enumerate(texts):
            text = text.removeprefix(buffer)
            if idx % 2 == 0 and text:
                new_nodes.append(
                    TextNode(text, TextType.TEXT)
                )
            elif text:
                new_nodes.append(
                    TextNode(text, text_type)
                )
    return new_nodes



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
