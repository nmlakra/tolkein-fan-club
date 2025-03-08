from enum import EnumType
import re

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

def block_to_block_type(markdown_text):
    heading_pattern = re.compile(r"^#{1,6}\s+(?=.*\S).+$")
    if heading_pattern.match(markdown_text):
        return BlockType.HEADING
    if markdown_text.startswith("```") and markdown_text.endswith("```"):
        return BlockType.CODE
    if all(line.startswith("> ") for line in markdown_text.split()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in markdown_text.split("\n")):
        return BlockType.UNORDERED_LIST
    if validate_markdown_ordered_list(markdown_text):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown_text):
    return markdown_text.strip().split("\n\n")
