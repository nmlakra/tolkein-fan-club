from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        if not self.text == other.text:
            return False
        if not self.text_type == other.text_type:
            return False
        if not self.url == other.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
