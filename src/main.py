import re
from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode
import os
import shutil


def remove_dir_content(dir_path):
    if os.path.exists(dir_path):
        dir_items = os.listdir(dir_path)
        for item in dir_items:
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                remove_dir_content(item_path)
                os.removedirs(item_path)

        print(f"Cleand {dir_path}!")
    else:
        print(f"{dir_path} doesn't exist!")

def copy_source_files_to_destination(src_path, dst_path):

    os.makedirs(dst_path, exist_ok=True)

    dir_items = os.listdir(src_path)
    for item in dir_items:
        item_src_path = os.path.join(src_path, item)
        item_dst_path = os.path.join(dst_path, item)
        if os.path.isfile(item_src_path):
            print(f"Moving {item_src_path} -> {item_dst_path}")
            shutil.copy2(item_src_path, item_dst_path)
        else:
            copy_source_files_to_destination(item_src_path, item_dst_path)

def copy_static_to_public():
    source_path = "./static"
    destination_path = "./public"

    if os.path.exists(destination_path):
        remove_dir_content(destination_path)

    copy_source_files_to_destination(source_path, destination_path)

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

def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()
