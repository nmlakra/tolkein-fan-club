import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = split_node_link(
        split_node_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([text_node], "_", TextType.ITALIC),
                    "**",
                    TextType.BOLD,
                ),
                "`",
                TextType.CODE,
            )
        )
    )

    return nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_node_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_images(node.text)
        if not links:
            new_nodes.append(node)
            text_array = [node.text]
        else:
            text_array = [node.text]
            while links:
                link_data = links.pop(0)  # ("alt_text", "https://link.com")
                split_str = f"![{link_data[0]}]({link_data[1]})"
                text_array = text_array.pop(0).split(split_str, maxsplit=1)
                if text_array and text_array[0]:
                    new_nodes.append(TextNode(text_array.pop(0), TextType.TEXT))
                new_nodes.append(TextNode(link_data[0], TextType.IMAGE, link_data[1]))

            # Appending the remianing text into the new_nodes array assuming it's not empty
            if text_array and text_array[-1]:
                if len(text_array) > 1:
                    raise Exception("FATAL ERROR!!!")
                new_nodes.append(TextNode(text_array.pop(), TextType.TEXT))

    return new_nodes


def split_node_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            text_array = [node.text]
        else:
            text_array = [node.text]
            while links:
                link_data = links.pop(0)  # ("alt_text", "https://link.com")
                split_str = f"[{link_data[0]}]({link_data[1]})"
                text_array = text_array.pop(0).split(split_str, maxsplit=1)
                if text_array and text_array[0]:
                    new_nodes.append(TextNode(text_array.pop(0), TextType.TEXT))
                new_nodes.append(TextNode(link_data[0], TextType.LINK, link_data[1]))

            # Appending the remianing text into the new_nodes array assuming it's not empty
            if text_array and text_array[-1]:
                if len(text_array) > 1:
                    raise Exception("FATAL ERROR!!!")
                new_nodes.append(TextNode(text_array.pop(), TextType.TEXT))
    return new_nodes


def validate_markdown(text, delimiter):

    delimiter_count = 0
    n = len(text)
    m = len(delimiter)
    for i in range(n):
        if text[i : i + m] == delimiter:
            delimiter_count += 1
    if delimiter_count % 2 != 0:
        return False
    return True


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not validate_markdown(node.text, delimiter):
            raise Exception("Invalid markdown syntax!")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        buffer = "    "
        texts = (buffer + node.text).split(delimiter)

        for idx, text in enumerate(texts):
            text = text.removeprefix(buffer)
            if idx % 2 == 0 and text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            elif text:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes
