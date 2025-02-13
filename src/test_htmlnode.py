import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode(prop={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.prop)

    def test_empty_prop(self):
        node = HTMLNode(prop={})

        self.assertEqual(node.props_to_html(), '')
