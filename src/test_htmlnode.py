import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode(prop={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), '''href="https://www.google.com" target="_blank"''')

    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.prop)

    def test_empty_prop(self):
        node = HTMLNode(prop={})

        self.assertEqual(node.props_to_html(), '')


class TestLeafNode(unittest.TestCase):

    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '''<a href="https://www.google.com">Click me!</a>''')

    def test_err(self):
        node = LeafNode(None, "This is a paragraph of text.")
        self.assertRaises(ValueError, node.to_html)

        node2 = LeafNode("p", None)
        self.assertRaises(ValueError, node2.to_html)

