import unittest

from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_node_link,
    split_node_image,
    text_to_textnode
)
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestTextToNode(unittest.TestCase):

    def base_case(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_values = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        print("Running text_to_node test")
        return_values = text_to_textnode(text)
        self.assertEqual(expected_values, return_values)

class TestSplitNodeImage(unittest.TestCase):

    def test_double_link_node(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text_node = TextNode(text, TextType.TEXT)
        expected_value = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        return_value = split_node_image([text_node])
        self.assertEqual(expected_value, return_value)


class TestSplitNodeLink(unittest.TestCase):

    def test_none_node(self):
        node = TextNode("", TextType.TEXT)
        expected_value = [node]
        return_value = split_node_link([node])
        self.assertEqual(expected_value, return_value)

    def test_single_link_node(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        text_node = TextNode(text, TextType.TEXT)
        expected_value = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        return_value = split_node_link([text_node])
        self.assertEqual(expected_value, return_value)

        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and something else!"
        text_node2 = TextNode(text2, TextType.TEXT)
        expected_value2 = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and something else!", TextType.TEXT),
        ]
        return_value2 = split_node_link([text_node2])
        self.assertEqual(expected_value2, return_value2)

    def test_double_link_node(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        expected_value = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        return_value = split_node_link([node])
        self.assertEqual(expected_value, return_value)


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_double_markdown_links(self):

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_value = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        return_value = extract_markdown_links(text)

        self.assertEqual(expected_value, return_value)


class TestExtractMarkdownImages(unittest.TestCase):

    def test_double_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_value = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        return_value = extract_markdown_images(text)

        self.assertEqual(expected_value, return_value)


class TestSplitNodesDeliminator(unittest.TestCase):

    def test_code_block(self):

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_word(self):

        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_italic_word(self):

        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start(self):

        node = TextNode("**bold** word at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" word at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter(self):

        node = TextNode("Text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("Text with no delimiter", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_invalid_markdown(self):

        node = TextNode("Invalid markdown *bold** syntax", TextType.BOLD)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_not_text_type(self):

        node = TextNode("*This is an italics sentence*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [node])

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


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
        leaf_node = LeafNode(
            "img", "", {"src": "https:boot.dev/random_img.png", "alt": "Alt text"}
        )
        img_leaf_node = text_node_to_html_node(img_node)
        self.assertEqual(img_node.text_type, TextType.IMAGE)
        self.assertIsInstance(img_leaf_node, LeafNode)
        self.assertEqual(leaf_node.__repr__(), img_leaf_node.__repr__())
