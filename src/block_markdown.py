from enum import EnumType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(EnumType):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "undordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    for block in blocks:
        if block.startswith("# "):
            return block.removeprefix("# ").lstrip()
    raise Exception("Title not found!")


def validate_markdown_ordered_list(text):
    lines = text.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            return False

    return True



def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown_text):
    blocks = markdown_text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def block_to_paragraph_node(markdown_block):
    markdown_block = " ".join(markdown_block.split("\n"))
    children_node = text_to_children(markdown_block)
    paragraph_node = ParentNode("p", children_node)
    return paragraph_node


def block_to_heading_node(markdown_block):
    heading_level = markdown_block.count("#")
    markdown_block = markdown_block.removeprefix("#" * heading_level).strip()
    children_nodes = text_to_children(markdown_block)
    heading_node = ParentNode(f"h{heading_level}", children_nodes)
    return heading_node


def block_to_quote_node(markdown_block):
    markdown_block = "".join(line.removeprefix(">").strip() for line in markdown_block.split("\n"))
    children_nodes = []
    children_nodes.append(text_to_children(markdown_block))
    children_nodes = text_to_children(markdown_block)
    quote_node = ParentNode("blockquote", children_nodes)
    return quote_node


def block_to_ulist_node(markdown_block):
    children_nodes = []
    for line in markdown_block.split("\n"):
        children_nodes.append(text_to_children(line.removeprefix("- ")))
    ulist_node = ParentNode(
        "ul", [ParentNode("li", ulist_item) for ulist_item in children_nodes]
    )
    return ulist_node


def block_to_olist_node(markdown_block):
    children_nodes = []
    for idx, line in enumerate(markdown_block.split("\n")):
        children_nodes.append(text_to_children(line.removeprefix(f"{idx + 1}. ")))
    olist_node = ParentNode(
        "ol", [ParentNode("li", olist_item) for olist_item in children_nodes]
    )
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
        block_type = block_to_block_type(markdown_block)
        if block_type == BlockType.CODE:
            child_nodes.append(block_to_codeblock_node(markdown_block))
        elif block_type == BlockType.HEADING:
            child_nodes.append(block_to_heading_node(markdown_block))
        elif block_type == BlockType.QUOTE:
            child_nodes.append(block_to_quote_node(markdown_block))
        elif block_type == BlockType.UNORDERED_LIST:
            child_nodes.append(block_to_ulist_node(markdown_block))
        elif block_type == BlockType.ORDERED_LIST:
            child_nodes.append(block_to_olist_node(markdown_block))
        elif block_type == BlockType.PARAGRAPH:
            child_nodes.append(block_to_paragraph_node(markdown_block))
        else:
            raise Exception(f"Invalid block type: {block_type}")

    return ParentNode("div", child_nodes)
