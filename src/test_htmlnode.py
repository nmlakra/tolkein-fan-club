import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode(
            prop={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), '''href="https://www.google.com" target="_blank"'''
        )

    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.prop)

    def test_empty_prop(self):
        node = HTMLNode(prop={})

        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):

    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node2.to_html(), """<a href="https://www.google.com">Click me!</a>"""
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text.")

    def test_to_html_no_value(self):
        node2 = LeafNode("p", None)
        self.assertRaises(ValueError, node2.to_html)

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


class TestParentNode(unittest.TestCase):

    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_inner_parent_eq(self):

        inner_parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node = ParentNode("html", [inner_parent_node])
        self.assertEqual(
            node.to_html(), "<html><p><b>Bold text</b>Normal text</p></html>"
        )

        node2 = ParentNode("html", [inner_parent_node, inner_parent_node])
        self.assertEqual(
            node2.to_html(),
            "<html><p><b>Bold text</b>Normal text</p><p><b>Bold text</b>Normal text</p></html>",
        )
