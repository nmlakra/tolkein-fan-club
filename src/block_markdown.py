from enum import EnumType
import re
from htmlnode import HTMLNode, ParentNode
from main import text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType

class BlockType(EnumType):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "qoute"
    UNORDERED_LIST = "undordered_list"
    ORDERED_LIST = "ordered_list"

def validate_markdown_ordered_list(text):
    lines = text.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            return False

    return True

def block_to_block_type(markdown_block):
    heading_pattern = re.compile(r"^#{1,6}\s+(?=.*\S).+$")
    if heading_pattern.match(markdown_block):
        return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith("> ") for line in markdown_block.split()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in markdown_block.split("\n")):
        return BlockType.UNORDERED_LIST
    if validate_markdown_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown_text):
    return markdown_text.strip().split("\n\n")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def block_to_paragraph_node(markdown_block):
    markdown_block = markdown_block.replace("\n", " ")
    children_node = text_to_children(markdown_block)
    paragraph_node = ParentNode("p", children_node)
    return paragraph_node

def block_to_heading_node(markdown_block):
    heading_level = markdown_block.count("#")
    markdown_block = markdown_block.removeprefix("#" * heading_level)
    children_nodes = text_to_children(markdown_block)
    heading_node = ParentNode(f"h{heading_level}", children_nodes)
    return heading_node

def block_to_qoute_node(markdown_block):
    children_nodes = []
    for line in markdown_block.split("\n"):
        children_nodes.append(text_to_children(line.removeprefix("> ")))
    children_nodes = text_to_children(markdown_block)
    qoute_node = ParentNode("blockqoute", children_nodes)
    return qoute_node

def block_to_ulist_node(markdown_block):
    children_nodes = []
    for line in markdown_block.split("\n"):
        children_nodes.append(text_to_children(line.removeprefix("- ")))
    ulist_node = ParentNode("ul", [ParentNode("li", ulist_item) for ulist_item in children_nodes])
    return ulist_node

def block_to_olist_node(markdown_block):
    children_nodes = []
    for idx, line in enumerate(markdown_block.split("\n")):
        children_nodes.append(text_to_children(line.removeprefix(f"{idx + 1}. ")))
    olist_node = ParentNode("ol", [ParentNode("li", olist_item) for olist_item in children_nodes])
    return olist_node

def block_to_codeblock_node(markdown_block):
    markdown_block = markdown_block.removeprefix("```\n").removesuffix("```")
    child_node = text_node_to_html_node(TextNode(markdown_block, TextType.CODE))
    codeblock_node = ParentNode("pre", [child_node])
    return codeblock_node

def markdown_to_html_node(markdown_text):
    markdown_blocks = markdown_to_blocks(markdown_text)
    child_nodes = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block )
        if block_type == BlockType.CODE:
            child_nodes.append(block_to_codeblock_node(markdown_block))
        elif block_type == BlockType.HEADING:
            child_nodes.append(block_to_heading_node(markdown_block))
        elif block_type == BlockType.QUOTE:
            child_nodes.append(block_to_qoute_node(markdown_block))
        elif block_type == BlockType.UNORDERED_LIST:
            child_nodes.append(block_to_ulist_node(markdown_block))
        elif block_type == BlockType.ORDERED_LIST:
            child_nodes.append(block_to_olist_node(markdown_block))
        elif block_type == BlockType.PARAGRAPH:
            child_nodes.append(block_to_paragraph_node(markdown_block))
        else:
            raise Exception(f"Invalid block type: {block_type}")

    return ParentNode("div", child_nodes)

