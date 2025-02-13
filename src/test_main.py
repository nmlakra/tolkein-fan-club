import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_link_node_to_html_node(self):
        link_node = TextNode(
            "Welcome to boot.dev!", TextType.LINK, "https://www.boot.dev"
        )
        leaf_node = LeafNode(
            "a", "Welcome to boot.dev!", prop={"href": "https://www.boot.dev"}
        )
        link_leaf_node = text_node_to_html_node(link_node)
        self.assertEqual(link_node.text_type, TextType.LINK)
        self.assertIsInstance(link_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), link_leaf_node.__repr__())

    def test_text_node_to_html_node(self):
        text_node = TextNode("Normal text", TextType.TEXT)
        leaf_node = LeafNode(None, "Normal text")
        text_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(text_node.text_type, TextType.TEXT)
        self.assertIsInstance(text_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), text_leaf_node.__repr__())

    def test_bold_node_to_html_node(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        leaf_node = LeafNode("b", "Bold text")
        bold_leaf_node = text_node_to_html_node(bold_node)
        self.assertEqual(bold_node.text_type, TextType.BOLD)
        self.assertIsInstance(bold_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), bold_leaf_node.__repr__())

    def test_italic_node_to_html_node(self):
        italic_node = TextNode("Italic text", TextType.ITALIC)
        leaf_node = LeafNode("i", "Italic text")
        italic_leaf_node = text_node_to_html_node(italic_node)
        self.assertEqual(italic_node.text_type, TextType.ITALIC)
        self.assertIsInstance(italic_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), italic_leaf_node.__repr__())


    def test_code_node_to_html_node(self):
        code_node = TextNode("Code text", TextType.CODE)
        leaf_node = LeafNode("code", "Code text")
        code_leaf_node = text_node_to_html_node(code_node)
        self.assertEqual(code_node.text_type, TextType.CODE)
        self.assertIsInstance(code_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), code_leaf_node.__repr__())


    def test_image_node_html_node(self):
        img_node = TextNode("Alt text", TextType.IMAGE, "https:boot.dev/random_img.png")
        leaf_node = LeafNode("img", "", {"src": "https:boot.dev/random_img.png", "alt": "Alt text"})
        img_leaf_node = text_node_to_html_node(img_node)
        self.assertEqual(img_node.text_type, TextType.IMAGE)
        self.assertIsInstance(img_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), img_leaf_node.__repr__())


